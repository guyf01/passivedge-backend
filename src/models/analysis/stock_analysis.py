"""Stock analysis result data."""

from dataclasses import dataclass, field
from typing import Any

from src.models.date import MonthPeriod
from .day_score import DayScore


@dataclass
class StockAnalysis:
    """
    Stock analysis result - works for both single and multi-month.
    
    For single month: period.start == period.end
    For multi-month: period.start < period.end
    
    :param symbol: Stock ticker symbol
    :param period: The period of the analysis
    :param days: Dict mapping day of month (1-31) to DayScore
    """
    symbol: str
    period: MonthPeriod
    days: dict[int, DayScore] = field(default_factory=dict)


    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        return {
            "symbol": self.symbol,
            "period": self.period.to_dict(),
            "days": {k: v.to_dict() for k, v in self.days.items()}
        }
