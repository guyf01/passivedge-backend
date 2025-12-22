"""Daily stock score data."""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass
class DayScore:
    """
    Daily stock score data.
    
    :param day: The day of the month (1-31)
    :param avg_price_diff: The average price difference for the day, or None if no data
    """
    day: int
    avg_price_diff: float | None


    @staticmethod
    def combine(scores: list[DayScore]) -> DayScore:
        """
        Combine multiple DayScore objects for the same day into one averaged result.
        
        :param scores: List of DayScore objects (must all have the same day)
        :return: New DayScore with averaged avg_price_diff
        :raises ValueError: If days don't match or scores is empty
        """
        if not scores:
            raise ValueError("Cannot combine empty scores list")
        
        day = scores[0].day
        total = 0.0
        count = 0
        
        for score in scores:
            if score.day != day:
                raise ValueError(f"All scores must have the same day. Expected {day}, got {score.day}")
            
            if score.avg_price_diff is not None:
                total += score.avg_price_diff
                count += 1
        
        if count == 0:
            return DayScore(day=day, avg_price_diff=None)
        
        return DayScore(day=day, avg_price_diff=round(total / count, 2))


    def to_dict(self) -> dict[str, Any]:
        """Convert to JSON-serializable dictionary."""
        result: dict[str, Any] = {"day": self.day}
        if self.avg_price_diff is not None:
            result["avg_price_diff"] = Decimal(str(self.avg_price_diff))
        return result
    
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> DayScore:
        """Create a DayScore from a dictionary."""
        avg = data.get("avg_price_diff")
        return cls(
            day=int(data["day"]),
            avg_price_diff=float(avg) if avg is not None else None
        )
