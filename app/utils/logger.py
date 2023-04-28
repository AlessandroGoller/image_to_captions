""" Module to configure logger """
import os
from datetime import datetime
from typing import Any

from loguru import logger

log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)


def configure_logger() -> Any:
    """Settings Logger"""
    logger.add(
        f"{log_folder}/{datetime.now().strftime('%Y-%m-%d')}.log", rotation="00:00"
    )
    return logger
