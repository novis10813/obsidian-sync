"""
Global dependencies for the FastAPI application.
"""

import sys
from loguru import logger
from .config import settings


def setup_logging() -> None:
    """Setup application logging."""
    logger.remove()
    logger.add(sys.stderr, level=settings.log_level)


# Initialize logging when module is imported
setup_logging() 