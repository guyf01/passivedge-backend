"""Month period model for date ranges."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from .month_date import MonthDate
from .exceptions import InvalidDateRangeError, InvalidDateError


MAX_PERIOD_MONTHS = 60


@dataclass(frozen=True)
class MonthPeriod:
    """
    Represents a period of one or more months.
    
    For single month: start == end
    For multi-month: start < end
    
    :param start: The start month of the period
    :param end: The end month of the period
    """
    start: MonthDate
    end: MonthDate


    def __post_init__(self):
        """Validate range."""
        if self.start > self.end:
            raise InvalidDateRangeError(
                f"End date {self.end} must be after or equal to start date {self.start}"
            )
        
        # Ensure end month has a next month
        try:
            self.end.next_month()
        except InvalidDateError:
            raise InvalidDateRangeError(
                f"End date {self.end} month cannot be current month"
            )
        
        total_months = (self.end.year - self.start.year) * 12 + (self.end.month - self.start.month)
        if total_months > MAX_PERIOD_MONTHS:
            raise InvalidDateRangeError(
                f"Period cannot exceed {MAX_PERIOD_MONTHS / 12} years({MAX_PERIOD_MONTHS} months). Current period: {total_months} months"
            )


    @classmethod
    def single(cls, month: MonthDate) -> MonthPeriod:
        """Create a single-month period."""
        return cls(start=month, end=month)


    def generate_months(self) -> Iterator[MonthDate]:
        """
        Generate all months in the period.
        
        :return: Generator of MonthDate objects from start to end (inclusive)
        """
        current = self.start
        
        while current <= self.end:
            yield current
            current = current.next_month()


    def to_dict(self) -> dict[str, str]:
        """Convert to JSON-serializable dictionary."""
        return {
            "start": str(self.start),
            "end": str(self.end)
        }


    @classmethod
    def from_dict(cls, data: dict[str, str]) -> MonthPeriod:
        """Create a MonthPeriod from a dictionary."""
        return cls(
            start=MonthDate.from_str(data["start"]),
            end=MonthDate.from_str(data["end"])
        )


    def __str__(self) -> str:
        """Return string representation of the period."""
        return f"{self.start} - {self.end}"
