from src.models.date import MonthDate
from src.models.analysis import StockAnalysis
from src import get_logger
from src.services.stock_fetcher.base_fetcher import StockFetcher
from .base_storage import CacheStorage


logger = get_logger('cache')


class CachingStockFetcher(StockFetcher):
    def __init__(self, inner: StockFetcher, storage: CacheStorage):
        self._inner = inner
        self._storage = storage

    def is_valid_symbol(self, symbol: str) -> bool:
        return self._inner.is_valid_symbol(symbol)

    def fetch(self, symbol: str, month: MonthDate) -> StockAnalysis:
        cached = self._storage.get(symbol, month)
        if cached is not None:
            logger.info(f"Cache HIT: '{symbol}' '{month}'")
            return cached

        logger.info(f"Cache MISS: '{symbol}' '{month}'")
        data = self._inner.fetch(symbol, month)
        self._storage.save(symbol, month, data)
        return data
