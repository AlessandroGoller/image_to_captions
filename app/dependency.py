"""
Module with the dependency
"""

from functools import lru_cache

from app.config.config import Config


@lru_cache()
def get_settings():  # type: ignore
    """ Return the config"""
    return Config()
