import logging
import sys
from src.config import settings

def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
