"""Stock analysis result data."""
from __future__ import annotations

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
            "days": {str(k): v.to_dict() for k, v in self.days.items()}
        }
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> StockAnalysis:
        """Create a StockAnalysis from a dictionary."""
        return cls(
            symbol=data["symbol"],
            period=MonthPeriod.from_dict(data["period"]),
            days={int(k): DayScore.from_dict(v) for k, v in data["days"].items()}
        )
