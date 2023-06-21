""" CRUD per telegram """

from typing import Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.dependency import get_db
from app.model.telegram import Telegram
from app.schema.telegram import TelegramCreate
from app.utils.logger import configure_logger

logger = configure_logger()

def get_telegram_by_user_id(id_user: int) -> Optional[Telegram]:
    """Return the Telegram from id_user"""
    db: Session = next(get_db())
    return db.query(Telegram).filter(Telegram.id_user == id_user).first()  # type: ignore

def get_telegram_by_user_tele_id(id_user_tele: int) -> Optional[Telegram]:
    """Return the Telegram from id_user"""
    db: Session = next(get_db())
    return db.query(Telegram).filter(Telegram.id_user_telegram == id_user_tele).first()  # type: ignore

def get_telegram_by_chat_id(id_chat: int) -> Optional[Telegram]:
    """Return the Telegram from id_user"""
    db: Session = next(get_db())
    return db.query(Telegram).filter(Telegram.id_chat == id_chat).first()  # type: ignore

def get_telegram_by_id(id_telegram: int) -> Optional[Telegram]:
    """Return the Telegram from id_telegram"""
    db: Session = next(get_db())
    return db.query(Telegram).filter(Telegram.id_telegram == id_telegram).first()  # type: ignore

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

def update_last_access(telegram: Telegram) -> None:
    """ Update last access """
    db: Session = next(get_db())
    telegram.last_access = func.now()
    db.merge(telegram)
    db.commit()

def delete_telegram_from_id_chat(id_chat: int) -> dict[str, bool]:
    """Permit to delete a telegram from an id_chat"""
    db: Session = next(get_db())
    telegram:Telegram = db.query(Telegram).filter_by(id_chat=id_chat).first()
    db.delete(telegram)
    db.commit()
    return {"ok": True}

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
