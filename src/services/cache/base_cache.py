"""Base cache class with cache-aside pattern."""

import logging
from abc import ABC, abstractmethod
from typing import Callable, TypeVar, Generic

from src.models.date import MonthDate


logger = logging.getLogger('cache')


T = TypeVar('T')


class BaseCache(ABC, Generic[T]):
    """
    Abstract cache with cache-aside pattern.
    
    Exposes a single get() method that handles cache hit/miss internally.
    On cache miss, calls the provided fetcher function and stores the result.
    
    :param fetcher: Callable that fetches data on cache miss
    """
    
    def __init__(self, fetcher: Callable[[str, MonthDate], T]):
        """
        Initialize cache with a data fetcher.
        
        :param fetcher: Function to call on cache miss (symbol, month) -> T
        """
        self._fetcher = fetcher


    def get(self, symbol: str, month: MonthDate) -> T:
        """
        Get data for a symbol and month.
        
        Checks cache first, fetches and caches on miss.
        
        :param symbol: Stock ticker symbol
        :param month: The month to get data for
        :return: Cached or freshly fetched data
        """
        # Try cache first
        cached = self._get_from_cache(symbol, month)
        if cached is not None:
            logger.info(f"Cache [bold green]HIT[/]: '{symbol}' '{month}'")
            return cached

        # Cache miss - fetch and store
        logger.info(f"Cache [bold yellow]MISS[/]: '{symbol}' '{month}'")
        data = self._fetcher(symbol, month)
        self._save_to_cache(symbol, month, data)

        return data


    @abstractmethod
    def _get_from_cache(self, symbol: str, month: MonthDate) -> T | None:
        """
        Get data from cache.
        
        :param symbol: Stock ticker symbol
        :param month: The month
        :return: Cached data or None if not found
        """
        pass


    @abstractmethod
    def _save_to_cache(self, symbol: str, month: MonthDate, data: T) -> None:
        """
        Save data to cache.
        
        :param symbol: Stock ticker symbol
        :param month: The month
        :param data: Data to cache
        """
        pass
