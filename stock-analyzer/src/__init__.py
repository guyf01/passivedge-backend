"""PassivEdge Backend - Stock analysis service."""

import logging, os


def _setup_logger() -> logging.Logger:
    # Clear existing handlers to avoid duplicate logging (caused by aws lambda)
    root = logging.getLogger()
    if root.hasHandlers():
        root.handlers.clear()

    # Create analyzer logger
    logger = logging.getLogger('analyzer')
    logger.setLevel(logging.INFO)

    # Use RichHandler locally, StreamHandler in Lambda
    if os.environ.get('AWS_LAMBDA_FUNCTION_NAME'):
        # Lambda - simple StreamHandler for CloudWatch
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(levelname)s %(name)s: %(message)s'))
    else:
        # Local - RichHandler for pretty output
        from rich.logging import RichHandler
        handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            omit_repeated_times=False
        )
        handler.setFormatter(logging.Formatter('%(name)s: %(message)s'))

    logger.addHandler(handler)
    logger.propagate = False

    return logger


BASE_LOGGER = _setup_logger()


def get_logger(name: str, parent: logging.Logger = BASE_LOGGER) -> logging.Logger:
    return parent.getChild(name)
