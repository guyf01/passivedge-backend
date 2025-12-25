"""API error types with RFC 7807 Problem Details format."""

import json
from enum import Enum


class ApiError(Enum):
    """
    API error types with HTTP status and title.
    """
    
    # --- validation_error (400) ---
    MISSING_BODY = (400, "validation_error", "Missing Request Body")
    INVALID_BODY = (400, "validation_error", "Invalid Request Body")
    INVALID_FORMAT = (400, "validation_error", "Invalid Format")
    INVALID_DATE = (400, "validation_error", "Invalid Date")
    INVALID_RANGE = (400, "validation_error", "Invalid Date Range")

    # --- not_found (404) ---
    SYMBOL_NOT_FOUND = (404, "not_found", "Symbol Not Found")
    NO_DATA = (404, "not_found", "No Data Found")

    # --- server_error (500) ---
    CONFIG_ERROR = (500, "server_error", "Configuration Error")
    SERVER_ERROR = (500, "server_error", "Internal Server Error")


    def __init__(self, status_code: int, error_type: str, title: str):
        self.status_code = status_code
        self.error_type = error_type
        self.title = title


    def response(self, detail: str) -> dict:
        """
        Generate API Gateway response in RFC 7807 format.
        
        :param detail: Specific error detail message
        :return: API Gateway response dict
        """
        return {
            'statusCode': self.status_code,
            'headers': {
                'Content-Type': 'application/problem+json',
                'Access-Control-Allow-Origin': 'https://passivedge.com',
                'X-Content-Type-Options': 'nosniff',
                'X-Frame-Options': 'DENY',
                'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
                'Cache-Control': 'no-store',
            },
            'body': json.dumps({
                'type': self.error_type,
                'title': self.title,
                'status': self.status_code,
                'detail': detail
            })
        }
