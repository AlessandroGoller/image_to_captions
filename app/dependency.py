"""
Module with the dependency
"""

from functools import lru_cache
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config.config import Config  # noqa type: ignore


@lru_cache()
def get_settings():  # type: ignore
    """Return the config"""
    return Config()


# Dependency
def get_db() -> Iterator:
    """Return an iterator to the db"""
    db = DBSessionLocal()
    try:
        yield db
    finally:
        db.close()


# DB
database = declarative_base()

database_engine = create_engine(
    get_settings().SQLALCHEMY_DATABASE_URI,
    echo=True,
)
DBSessionLocal = sessionmaker(
    autocommit=False, autoflush=True, binds={database: database_engine}
)
