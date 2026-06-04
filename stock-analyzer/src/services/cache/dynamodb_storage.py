import boto3
from botocore.exceptions import ClientError

from src.models.date import MonthDate
from src.models.analysis import StockAnalysis
from src import get_logger
from .base_storage import CacheStorage


logger = get_logger('dynamodb_storage')


class DynamoDBStorage(CacheStorage):
    def __init__(self, table_name: str, partition_key: str, sort_key: str):
        self._table = boto3.resource('dynamodb').Table(table_name)
        self._partition_key = partition_key
        self._sort_key = sort_key


    def get(self, symbol: str, month: MonthDate) -> StockAnalysis | None:
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


    def save(self, symbol: str, month: MonthDate, data: StockAnalysis) -> None:
        try:
            self._table.put_item(
                Item={
                    self._partition_key: symbol,
                    self._sort_key: str(month),
                    **data.to_dict()
                }
            )
            logger.info(f"Cache WRITE for '{symbol}' '{month}'")
        except ClientError as e:
            logger.error(f"Cache WRITE error for '{symbol}' '{month}': {e}")
