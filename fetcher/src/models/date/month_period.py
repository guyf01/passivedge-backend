"""Month period model for date ranges."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterator

from .month_date import MonthDate
from .exceptions import InvalidDateRangeError, InvalidDateError


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
            "start": self.start.to_dict(),
            "end": self.end.to_dict()
        }


    @classmethod
    def from_dict(cls, data: dict[str, str]) -> MonthPeriod:
        """Create a MonthPeriod from a dictionary."""
        return cls(
            start=MonthDate.from_dict(data["start"]),
            end=MonthDate.from_dict(data["end"])
        )
