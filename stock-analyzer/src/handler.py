"""AWS Lambda handler for stock analysis API."""

import json, os
from typing import Any

from src.models.date import MonthDate, MonthPeriod
from src.models.date.exceptions import MonthDateError, InvalidDateRangeError
from src.services.stock_fetcher import MonthStockFetcher, NoDataForMonthError
from src.services.cache import DynamoDBCache
from src.services.aggregator import StockAggregator
from src.errors import ApiError
from src import get_logger


logger = get_logger('handler')


def handler(event: dict, context: Any) -> dict:
    """
    Lambda handler for stock analysis.
    
    POST body (JSON):
        - symbol: Stock ticker (e.g., AAPL)
        - start: Start month (YYYY-MM format)
        - end: End month (YYYY-MM format)
    """
    logger.info("Handler called")

    try:
        # Parse JSON body
        body = event.get('body')
        if not body:
            logger.error("Missing request body")
            return ApiError.MISSING_BODY.response("Missing request body")
        
        try:
            body = json.loads(body)
        except json.JSONDecodeError:
            logger.error("Body is not a valid JSON")
            return ApiError.INVALID_BODY.response("Body is not a valid JSON")

        logger.info(f"Request: {body}")

        required_params = {'symbol', 'start', 'end'}
        if not required_params.issubset(body):
            missing_params = required_params.difference(body)
            logger.error(f"Missing required parameters: {missing_params}")
            return ApiError.INVALID_BODY.response(
                f"Missing required parameters: {missing_params}"
            )

        # Parse dates
        try:
            start_date = MonthDate.from_str(body['start'])
            end_date = MonthDate.from_str(body['end'])
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
        symbol = body['symbol'].upper()
        if not fetcher.exists(symbol):
            logger.error(f"Symbol does not exist: {symbol}")
            return ApiError.SYMBOL_NOT_FOUND.response(f"Symbol does not exist: {symbol}")

        # Aggregate data
        aggregator = StockAggregator(
            fetcher=DynamoDBCache(
                table_name=os.environ['DYNAMODB_TABLE_NAME']
            )(fetcher.fetch)
        )
        try:
            logger.info(f"Analyzing '{symbol}' over {period}")
            result = aggregator.aggregate(symbol, period)
        except NoDataForMonthError as e:
            logger.error(f"No data for symbol: {e}")
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
