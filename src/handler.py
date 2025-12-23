"""AWS Lambda handler for stock analysis API."""

import json, os, logging
from typing import Any

from src.models.date import MonthDate, MonthPeriod
from src.models.date.exceptions import MonthDateError, InvalidDateRangeError
from src.services.stock_fetcher import MonthStockFetcher, NoDataForMonthError
from src.services.cache import DynamoDBCache
from src.services.aggregator import StockAggregator
from src.errors import ApiError


logger = logging.getLogger('handler')


def handler(event: dict, context: Any) -> dict:
    """
    Lambda handler for stock analysis.
    
    Query params:
        - symbol: Stock ticker (e.g., AAPL)
        - start: Start month (YYYY-MM format)
        - end: End month (YYYY-MM format)
    """
    logger.info("Handler called")

    logger.info(f"Event: {event}")
    params = event.get('queryStringParameters') or {}

    required_params = {'symbol', 'start', 'end'}
    if not required_params.issubset(params):
        missing_params = required_params.difference(params)
        logger.error(f"Missing required parameters: {missing_params}")
        return ApiError.MISSING_PARAM.response(
            f"Missing required parameters: {missing_params}"
        )

    # Parse dates
    try:
        start_date = MonthDate.from_str(params['start'])
        end_date = MonthDate.from_str(params['end'])
    except MonthDateError as e:
        logger.error(f"Invalid date: {e}")
        return ApiError.INVALID_DATE.response(str(e))

    # Create period
    try:
        period = MonthPeriod(start_date, end_date)
    except InvalidDateRangeError as e:
        logger.error(f"Invalid date range: {e}")
        return ApiError.INVALID_RANGE.response(str(e))

    # Check if stock exists
    fetcher = MonthStockFetcher()
    if not fetcher.exists(params['symbol']):
        logger.error(f"Stock '{params['symbol']}' does not exist")
        return ApiError.NO_DATA.response(f"Stock {params['symbol']} does not exist")

    # Aggregate data
    cache = DynamoDBCache(fetcher=fetcher.fetch, table_name=os.environ['DYNAMODB_TABLE_NAME'])
    aggregator = StockAggregator(fetcher=cache.get)
    try:
        logger.info(f"Analyzing '{params['symbol']}' over {period}")
        result = aggregator.aggregate(params['symbol'], period)
    except NoDataForMonthError as e:
        return ApiError.NO_DATA.response(str(e))
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        return ApiError.SERVER_ERROR.response(str(e))

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(result.to_dict())
    }
