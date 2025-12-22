"""DynamoDB cache implementation."""

import os
from typing import Callable

import boto3
from botocore.exceptions import ClientError

from src.models.date import MonthDate
from src.models.analysis import StockAnalysis
from .base_cache import BaseCache


class DynamoDBCache(BaseCache[StockAnalysis]):
    """
    DynamoDB implementation of cache for StockAnalysis.
    
    Table schema:
        - pk (String): Partition key, format: "STOCK#{symbol}"
        - sk (String): Sort key, format: "{year}-{month:02d}"
        - data (Map): StockAnalysis as dict
    """

    def __init__(
        self, 
        fetcher: Callable[[str, MonthDate], StockAnalysis],
        table_name: str | None = None
    ):
        """
        Initialize DynamoDB cache.
        
        :param fetcher: Function to call on cache miss
        :param table_name: DynamoDB table name (defaults to DYNAMODB_TABLE_NAME env var)
        """
        super().__init__(fetcher)
        
        self._table_name = table_name or os.environ.get('DYNAMODB_TABLE_NAME')
        if not self._table_name:
            raise ValueError(
                "DynamoDB table name required. "
                "Set DYNAMODB_TABLE_NAME env var or pass table_name."
            )
        
        self._table = boto3.resource('dynamodb').Table(self._table_name)


    def _get_from_cache(self, symbol: str, month: MonthDate) -> StockAnalysis | None:
        """Get StockAnalysis from DynamoDB."""
        try:
            response = self._table.get_item(
                Key={
                    'pk': symbol,
                    'sk': month.as_sk()
                }
            )
            
            item = response.get('Item')
            if not item:
                return None
            
            return StockAnalysis.from_dict(item['data'])
            
        except ClientError:
            return None


    def _save_to_cache(self, symbol: str, month: MonthDate, stock_analysis: StockAnalysis) -> None:
        """Save StockAnalysis to DynamoDB."""
        try:
            self._table.put_item(
                Item={
                    'pk': symbol,
                    'sk': month.as_sk(),
                    'data': stock_analysis.to_dict()
                }
            )
        except ClientError:
            pass  # Silently fail on cache write errors
