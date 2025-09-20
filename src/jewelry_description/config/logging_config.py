import sys
from loguru import logger
from typing import Optional

def logging_config(log_file: Optional[str] = None) -> None:
    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG",
        colorize=True,
        format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}:{function}:{line}</cyan> - <white>{message}</white> | {extra}",
    )
    if log_file:
        logger.add(
            log_file,
            level="DEBUG",
            format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level: <8} | {name}:{function}:{line} - {message} | {extra}",
            rotation="10 MB",
            retention=1,
            enqueue=True,
            serialize=False,
        )
