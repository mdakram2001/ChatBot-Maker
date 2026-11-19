import logging
import sys

from chatamu.config.settings import settings

def setup_logger() -> logging.Logger:

    logger = logging.getLogger("chatamu")

    if logger.handlers:
        return logger

    logger.setLevel(settings.LOG_LEVEL.upper())

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger

logger = setup_logger()