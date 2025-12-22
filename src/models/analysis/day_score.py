"""Daily stock score data."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass
class DayScore:
    """
    Daily stock score data.
    
    :param avg_price_diff: The average price difference for the day, or None if no data
    """
    avg_price_diff: float | None


    @staticmethod
    def combine(scores: list[DayScore]) -> DayScore:
        """
        Combine multiple DayScore objects into one averaged result.
        
        :param scores: List of DayScore objects
        :return: New DayScore with averaged avg_price_diff
        :raises ValueError: If scores is empty
        """
        if not scores:
            raise ValueError("Cannot combine empty scores list")
        
        total = 0.0
        count = 0
        
        for score in scores:
            if score.avg_price_diff is not None:
                total += score.avg_price_diff
                count += 1
        
        if count == 0:
            return DayScore(avg_price_diff=None)
        
        return DayScore(avg_price_diff=round(total / count, 2))


    def to_dict(self) -> dict[str, str]:
        """Convert to JSON-serializable dictionary."""
        if self.avg_price_diff is not None:
            return {"avg_price_diff": str(self.avg_price_diff)}
        return {}
    
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> DayScore:
        """Create a DayScore from a dictionary."""
        avg = data.get("avg_price_diff")
        return cls(
            avg_price_diff=float(avg) if avg is not None else None
        )
