"""Custom exceptions for MonthDate validation."""


class MonthDateError(ValueError):
    """Base exception for MonthDate errors."""
    pass


class InvalidDateError(MonthDateError):
    """Raised when date values are invalid (month, year, or not in history)."""
    pass


class InvalidDateRangeError(MonthDateError):
    """Raised when end date is before start date."""
    pass
