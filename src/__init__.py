"""PassivEdge Backend - Stock analysis service."""

import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[RichHandler(rich_tracebacks=True, markup=True)]
)
