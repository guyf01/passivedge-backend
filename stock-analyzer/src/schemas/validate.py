"""Request schemas for API endpoints."""

import json

from src import get_logger
from src.models.date import MonthDate, MonthPeriod


logger = get_logger("validator")


class ValidateRequest:
    """
    Request schema for /validate requests.
    
    Takes raw request body string, validates it, and exposes symbol and period.
    Raises ValueError on validation failure.
    """
    def __init__(self, raw_body: str | None):
        """
        Initialize ValidateRequest.
        
        :param raw_body: Raw request body string.
        """
        body = self._parse_body(raw_body)

        logger.info(f"Validating request: {body}")

        self.symbol = self._parse_symbol(body)
        self.period = self._parse_period(body)

        logger.info(f"Validated request: {self}")


    def __str__(self) -> str:
        return f"{self.symbol} ({self.period})"


    def _parse_body(self, raw_body: str | None) -> dict:
        """
        Parse raw request body string.
        
        :param raw_body: Raw request body string.
        :return: Parsed request body as dictionary.
        """
        if not raw_body:
            raise ValueError("Missing request body")
        
        try:
            body = json.loads(raw_body)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON body")
        
        if not isinstance(body, dict):
            raise ValueError("Request body must be a JSON object")
        
        return body


    def _parse_symbol(self, body: dict) -> str:
        """
        Parse symbol from request body.
        
        :param body: Parsed request body as dictionary.
        :return: Symbol as string.
        """
        if 'symbol' not in body:
            raise ValueError("Missing required field: symbol")
        return body['symbol'].upper()


    def _parse_period(self, body: dict) -> MonthPeriod:
        """
        Parse period from request body.
        
        :param body: Parsed request body as dictionary.
        :return: Period as MonthPeriod.
        """
        if 'start' not in body:
            raise ValueError("Missing required field: start")
        if 'end' not in body:
            raise ValueError("Missing required field: end")
        
        start = MonthDate.from_str(body['start'])
        end = MonthDate.from_str(body['end'])
        return MonthPeriod(start, end)
