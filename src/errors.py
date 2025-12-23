"""API error types with RFC 7807 Problem Details format."""

import json
from enum import Enum


class ApiError(Enum):
    """
    API error types with HTTP status and title.
    """
    # Validation errors (400)
    MISSING_PARAM = (400, "missing_parameter", "Missing Required Parameter")
    INVALID_FORMAT = (400, "invalid_format", "Invalid Format")
    INVALID_DATE = (400, "invalid_date", "Invalid Date")
    INVALID_RANGE = (400, "invalid_range", "Invalid Date Range")
    
    # Not found (404)
    NO_DATA = (404, "no_data", "No Data Found")
    
    # Server errors (500)
    CONFIG_ERROR = (500, "configuration_error", "Configuration Error")
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
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'type': self.error_type,
                'title': self.title,
                'status': self.status_code,
                'detail': detail
            })
        }
