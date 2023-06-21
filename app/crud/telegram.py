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

def delete_telegram(telegram: Telegram) -> dict[str, bool]:
    """Permit to delete a telegram"""
    db: Session = next(get_db())
    db.delete(telegram)
    db.commit()
    return {"ok": True}

def delete_all_telegram(id_user:int) -> None:
    """ Delete all telegram account connected to a id_user """
    db: Session = next(get_db())
    # Get all Telegram accounts connected to the user
    telegrams: list[Telegram] = db.query(Telegram).filter_by(id_user=id_user).all()
    # Delete each Telegram account
    for telegram in telegrams:
        try:
            delete_telegram_with_sessione(db, telegram)
        except Exception as error:
            logger.error(f"Error during deletion of the telegram post {telegram.posturl}\n{error}")

def delete_telegram_with_sessione(db:Session, telegram:Telegram)->None:
    """ Permit to delete a telegram with an already started session """
    db.delete(telegram)
    db.commit()