""" CRUD per telegram """

from typing import Optional

from sqlalchemy.orm import Session

from app.dependency import get_db
from app.model.telegram import Telegram
from app.schema.telegram import TelegramCreate
from app.utils.logger import configure_logger

logger = configure_logger()

def get_telegram_by_user_id(id_user: int) -> Optional[Telegram]:
    """Return the Telegram from id_user"""
    db: Session = next(get_db())
    return db.query(Telegram).filter(Telegram.id_user == id_user).first()  # type: ignore

def get_telegram_hash_by_user_id(id_user: int) -> Optional[Telegram]:
    """Return the Telegram Hash from id_user"""
    db: Session = next(get_db())
    return db.query(Telegram.unique_hash_code).filter(Telegram.id_user == id_user).first()  # type: ignore

def get_telegram_by_id(id_telegram: int) -> Optional[Telegram]:
    """Return the Telegram from id_telegram"""
    db: Session = next(get_db())
    return db.query(Telegram).filter(Telegram.id_telegram == id_telegram).first()  # type: ignore

def get_telegram_hash_by_id(id_telegram: int) -> Optional[Telegram]:
    """Return the Telegram Hash from id_telegram"""
    db: Session = next(get_db())
    return db.query(Telegram.unique_hash_code).filter(Telegram.id_telegram == id_telegram).first()  # type: ignore

def create_telegram(telegram: TelegramCreate) -> Telegram:
    """Creation a telegram, in input the schema of telegram create and return the telegram"""
    db: Session = next(get_db())
    db_telegram = Telegram(
        id_user=telegram.id_user,
    )
    db.add(db_telegram)
    db.commit()
    db.refresh(db_telegram)
    return db_telegram
