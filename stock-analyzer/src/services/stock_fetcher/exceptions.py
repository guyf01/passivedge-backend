"""Custom exceptions for stock fetcher service."""


class StockFetcherError(Exception):
    """Base exception for stock fetcher errors."""
    pass


class NoDataForMonthError(StockFetcherError):
    """Raised when no data is available for a specific month."""
    pass
