import sys
from typing import Optional
from loguru import logger


def setup_logging(log_file: Optional[str] = None) -> None:
    """
    Centralized logging configuration.

    Args:
        log_file: Path to log file. If not specified, logging will be console-only.
    """
    # Remove default loguru handler
    logger.remove()

    # Add handler for console output (DEBUG and above)
    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> - <white>{message}</white> | {extra}",
    )

    if log_file:
        # Add handler for file writing
        logger.add(
            log_file,
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} | {extra}",
            rotation="10 MB",
            retention=1,
            enqueue=True,
            serialize=False,
        )
