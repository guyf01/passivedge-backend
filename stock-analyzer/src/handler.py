"""AWS Lambda handler for stock analysis API using Lambda Powertools."""

import json, os
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError, ServiceError

from src.models.date import MonthDate, MonthPeriod
from src.models.date.exceptions import MonthDateError, InvalidDateRangeError
from src.services.stock_fetcher import MonthStockFetcher, NoDataForMonthError
from src.services.cache import DynamoDBCache
from src.services.aggregator import StockAggregator
from src import get_logger


logger = get_logger('handler')

app = APIGatewayRestResolver(
    cors=CORSConfig(
        allow_origin=os.environ.get('CORS_ORIGIN')
    )
)


# Catch-all exception handler - logs all errors automatically
@app.exception_handler(ServiceError)
def log_service_errors(ex: ServiceError):
    logger.error(f"{ex.__class__.__name__}: {ex}")
    raise


@app.exception_handler(Exception)
def log_unhandled_errors(ex: Exception):
    logger.exception(f"Unhandled error: {ex}")
    raise


@app.post("/analyze")
def analyze():
    """
    Analyze stock data for a given symbol and date range.
    
    POST body (JSON):
        - symbol: Stock ticker (e.g., AAPL)
        - start: Start month (YYYY-MM format)
        - end: End month (YYYY-MM format)
    """
    # Validate request body
    raw_body = app.current_event.body
    if not raw_body:
        raise BadRequestError("Missing request body")
    
    try:
        body = app.current_event.json_body
    except json.JSONDecodeError:
        raise BadRequestError("Invalid JSON body")
    
    logger.info(f"Request: {body}")

    if not isinstance(body, dict):
        raise BadRequestError("Request body must be a JSON object")

    # Validate required parameters
    required_params = {'symbol', 'start', 'end'}
    if not required_params.issubset(body):
        missing = required_params.difference(body)
        raise BadRequestError(f"Missing required parameters: {missing}")

    # Parse dates
    try:
        start_date = MonthDate.from_str(body['start'])
        end_date = MonthDate.from_str(body['end'])
    except MonthDateError as e:
        raise BadRequestError(f"Invalid date: {e}")

    # Create period
    try:
        period = MonthPeriod(start_date, end_date)
    except InvalidDateRangeError as e:
        raise BadRequestError(f"Invalid date range: {e}")

    # Check if stock exists
    fetcher = MonthStockFetcher()
    symbol = body['symbol'].upper()
    if not fetcher.exists(symbol):
        raise NotFoundError(f"Symbol does not exist: {symbol}")

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
        raise NotFoundError(str(e))

    return result.to_dict()


def handler(event, context):
    """Lambda entry point."""
    return app.resolve(event, context)
