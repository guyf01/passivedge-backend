"""PassivEdge Backend - Stock analysis service."""

import logging
from rich.logging import RichHandler


def _setup_logger() -> logging.Logger:
    # Clear existing handlers to avoid duplicate logging(caused by aws lambda)
    root = logging.getLogger()
    if root.hasHandlers():
        root.handlers.clear()

    # Create analyzer logger with RichHandler
    logger = logging.getLogger('analyzer')
    logger.setLevel(logging.INFO)

    # Add RichHandler to analyzer logger only
    handler = RichHandler(
        rich_tracebacks=True,
        markup=True,
        omit_repeated_times=False
    )
    handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))
    logger.addHandler(handler)

    # Prevent propagation to root logger (avoids duplicate logs)
    logger.propagate = False

    return logger


BASE_LOGGER = _setup_logger()


def get_logger(name: str, parent: logging.Logger = BASE_LOGGER) -> logging.Logger:
    return parent.getChild(name)
