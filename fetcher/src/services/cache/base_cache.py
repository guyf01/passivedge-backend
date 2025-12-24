"""Base cache class with cache-aside pattern."""

import logging
from abc import ABC, abstractmethod
from functools import wraps
from typing import Callable

from src.models.date import MonthDate
from src.models.analysis import StockAnalysis


logger = logging.getLogger('cache')


class BaseCache(ABC):
    """
    Abstract cache with cache-aside pattern.
    """
    def __call__(self, func: Callable[[str, MonthDate], StockAnalysis]) -> Callable[[str, MonthDate], StockAnalysis]:
        """
        Decorator that adds caching to a function.
        """
        @wraps(func)
        def wrapper(symbol: str, month: MonthDate) -> StockAnalysis:
            # Try cache first
            cached = self._get_from_cache(symbol, month)
            if cached is not None:
                logger.info(f"Cache [bold green]HIT[/]: '{symbol}' '{month}'")
                return cached

            # Cache miss - fetch and store
            logger.info(f"Cache [bold yellow]MISS[/]: '{symbol}' '{month}'")
            data = func(symbol, month)
            self._save_to_cache(symbol, month, data)
            return data

        return wrapper


    @abstractmethod
    def _get_from_cache(self, symbol: str, month: MonthDate) -> StockAnalysis | None:
        """
        Get data from cache.
        
        :param symbol: Stock ticker symbol
        :param month: The month
        :return: Cached data or None if not found
        """
        pass


    @abstractmethod
    def _save_to_cache(self, symbol: str, month: MonthDate, data: StockAnalysis):
        """
        Save data to cache.
        
        :param symbol: Stock ticker symbol
        :param month: The month
        :param data: Data to cache
        """
        pass
