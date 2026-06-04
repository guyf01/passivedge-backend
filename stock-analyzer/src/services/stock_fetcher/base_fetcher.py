from abc import ABC, abstractmethod

from src.models.date import MonthDate
from src.models.analysis import StockAnalysis


class StockFetcher(ABC):
    @abstractmethod
    def fetch(self, symbol: str, month: MonthDate) -> StockAnalysis: ...

    @abstractmethod
    def is_valid_symbol(self, symbol: str) -> bool: ...
