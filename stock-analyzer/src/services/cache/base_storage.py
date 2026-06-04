from abc import ABC, abstractmethod

from src.models.date import MonthDate
from src.models.analysis import StockAnalysis


class CacheStorage(ABC):
    @abstractmethod
    def get(self, symbol: str, month: MonthDate) -> StockAnalysis | None: ...

    @abstractmethod
    def save(self, symbol: str, month: MonthDate, data: StockAnalysis) -> None: ...
