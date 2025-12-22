"""PassivEdge Backend - Stock analysis service."""

import logging
from rich.logging import RichHandler

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s: %(message)s',
    handlers=[RichHandler(
        rich_tracebacks=True, 
        markup=True,
        omit_repeated_times=False
    )]
)
