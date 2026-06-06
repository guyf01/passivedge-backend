"""Request parsing for API endpoints."""

import json
from dataclasses import dataclass

from src import get_logger
from src.models.date import MonthDate, MonthPeriod


logger = get_logger("parsing")


@dataclass(frozen=True)
class AnalyzeRequest:
    symbol: str
    period: MonthPeriod


def parse_analyze_request(raw_body: str | None) -> AnalyzeRequest:
    """
    Parse and validate a raw POST body into an AnalyzeRequest.

    :param raw_body: Raw JSON string from the request body.
    :return: Validated AnalyzeRequest.
    :raises ValueError: If the body is missing, malformed, or fields are invalid.
    """
    logger.info("Parsing analyze request")

    body = _parse_body(raw_body)
    request = AnalyzeRequest(
        symbol=_parse_symbol(body),
        period=_parse_period(body),
    )

    logger.info(f"Parsed request: {request.symbol} ({request.period})")
    return request


def _parse_body(raw_body: str | None) -> dict:
    if not raw_body:
        raise ValueError("Missing request body")
    try:
        body = json.loads(raw_body)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON body")
    if not isinstance(body, dict):
        raise ValueError("Request body must be a JSON object")
    return body


def _parse_symbol(body: dict) -> str:
    if 'symbol' not in body:
        raise ValueError("Missing required field: symbol")
    return body['symbol'].upper()


def _parse_period(body: dict) -> MonthPeriod:
    if 'start' not in body:
        raise ValueError("Missing required field: start")
    if 'end' not in body:
        raise ValueError("Missing required field: end")
    return MonthPeriod(MonthDate.from_str(body['start']), MonthDate.from_str(body['end']))
