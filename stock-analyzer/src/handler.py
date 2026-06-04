"""AWS Lambda handler for stock analysis API using Lambda Powertools."""

import os
from aws_lambda_powertools.event_handler import APIGatewayRestResolver, CORSConfig
from aws_lambda_powertools.event_handler.exceptions import BadRequestError, NotFoundError, ServiceError

from src.schemas import ValidateRequest
from src.services.stock_fetcher import YahooStockFetcher, NoDataForMonthError
from src.services.cache import CachingStockFetcher, DynamoDBStorage
from src.services.aggregator import StockAggregator
from src import get_logger


logger = get_logger('handler')

app = APIGatewayRestResolver(
    cors=CORSConfig(
        allow_origin=os.environ.get('CORS_ORIGIN')
    )
)


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
    try:
        request = ValidateRequest(app.current_event.body)
    except ValueError as e:
        raise BadRequestError(str(e))
    
    fetcher = YahooStockFetcher()
    if not fetcher.is_valid_symbol(request.symbol):
        raise NotFoundError(f"Symbol does not exist: {request.symbol}")

    aggregator = StockAggregator(
        fetcher=CachingStockFetcher(
            inner=fetcher,
            storage=DynamoDBStorage(
                table_name=os.environ['DYNAMODB_TABLE_NAME'],
                partition_key=os.environ['DYNAMODB_PK'],
                sort_key=os.environ['DYNAMODB_SK'],
            ),
        )
    )
    
    try:
        logger.info(f"Analyzing '{request.symbol}' over {request.period}")
        result = aggregator.aggregate(request.symbol, request.period)
    except NoDataForMonthError as e:
        raise NotFoundError(str(e))

    return result.to_dict()


def handler(event, context):
    """Lambda entry point."""
    return app.resolve(event, context)
