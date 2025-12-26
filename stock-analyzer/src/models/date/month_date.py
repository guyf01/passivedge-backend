"""MonthDate dataclass for handling month/year with validation."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from .exceptions import InvalidDateError


# Module-level constants for current date (set at import time)
_now = datetime.now()
CURRENT_YEAR = _now.year
CURRENT_MONTH = _now.month


@dataclass(frozen=True, order=True)
class MonthDate:
    """
    Represents a specific month and year with validation.
    
    Validates that month/year are valid and represent a completed past month.
    
    :param year: The year (up to current year)
    :param month: The month (1-12)
    """
    year: int
    month: int


    def __post_init__(self):
        """
        Validate that month/year are valid and in known history.
        
        :raises InvalidDateError: If month, year, or date is invalid
        """
        # Validate month range
        if not isinstance(self.month, int) or self.month < 1 or self.month > 12:
            raise InvalidDateError(f"Invalid month: {self.month}. Must be 1-12.")
        
        # Validate year range
        if not isinstance(self.year, int) or self.year > CURRENT_YEAR:
            raise InvalidDateError(f"Invalid year: {self.year}. Must be {CURRENT_YEAR} or earlier.")
        
        # Validate it's a completed past month (known history)
        if (self.year, self.month) > (CURRENT_YEAR, CURRENT_MONTH):
            raise InvalidDateError(
                f"Month {self} is not history. Must be before {CURRENT_YEAR}-{CURRENT_MONTH:02d}."
            )


    def next_month(self) -> MonthDate:
        """
        Get the next month.
        
        :return: New MonthDate for next month
        """
        if self.month == 12:
            return MonthDate(year=self.year + 1, month=1)
        else:
            return MonthDate(year=self.year, month=self.month + 1)


    def to_datetime(self) -> datetime:
        """Convert to datetime object."""
        return datetime(self.year, self.month, 1)


    def __str__(self) -> str:
        """Convert to string in format 'YYYY-MM'."""
        return f"{self.year}-{self.month:02d}"


    @staticmethod
    def from_str(date_str: str) -> MonthDate:
        """Convert from string in format 'YYYY-MM'."""
        try:
            year, month = map(int, date_str.split('-'))
        except ValueError as e:
            raise InvalidDateError(f"Invalid date string: {date_str}")

        return MonthDate(year=year, month=month)
