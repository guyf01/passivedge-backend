"""DynamoDB cache implementation."""

import boto3
from botocore.exceptions import ClientError

from src.models.date import MonthDate
from src.models.analysis import StockAnalysis
from .base_cache import BaseCache, logger
from src import get_logger


logger = get_logger('dynamodb', logger)


class DynamoDBCache(BaseCache):
    """
    DynamoDB implementation of cache for StockAnalysis.
    """

    def __init__(
        self, 
        table_name: str,
        partition_key: str = 'symbol',
        sort_key: str = 'date'
    ):
        """
        Initialize DynamoDB cache.
        
        :param table_name: DynamoDB table name
        """
        super().__init__()

        self._table = boto3.resource('dynamodb').Table(table_name)
        self._partition_key = partition_key
        self._sort_key = sort_key


    def _get_from_cache(self, symbol: str, month: MonthDate) -> StockAnalysis | None:
        """
        Get StockAnalysis from DynamoDB.

        :param symbol: Stock symbol
        :param month: MonthDate object
        :return: StockAnalysis object or if not found None
        """
        try:
            response = self._table.get_item(
                Key={
                    self._partition_key: symbol,
                    self._sort_key: str(month)
                }
            )
            
            item = response.get('Item')
            if not item:
                return None
            
            return StockAnalysis.from_dict(item)
            
        except ClientError as e:
            logger.error(f"Cache READ error for '{symbol}' '{month}': {e}")
            return None


    def _save_to_cache(self, symbol: str, month: MonthDate, stock_analysis: StockAnalysis):
        """
        Save StockAnalysis to DynamoDB.

        :param symbol: Stock symbol
        :param month: MonthDate object
        :param stock_analysis: StockAnalysis object
        """
        try:
            self._table.put_item(
                Item={
                    self._partition_key: symbol,
                    self._sort_key: str(month),
                    **stock_analysis.to_dict()
                }
            )
            logger.info(f"Cache WRITE for '{symbol}' '{month}'")
        except ClientError as e:
            logger.error(f"Cache WRITE error for '{symbol}' '{month}': {e}")
