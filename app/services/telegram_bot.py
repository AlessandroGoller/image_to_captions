""" Telegram """

from typing import Optional

from app.crud.telegram import create_telegram, get_telegram_by_user_id
from app.dependency import get_settings
from app.model.telegram import Telegram
from app.schema.telegram import TelegramCreate
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

def get_telegram_url(user_id: str)->str:
    """ Return the url for telegram connection """
    telegram: Optional[Telegram] = get_telegram_by_user_id(id_user=int(user_id))
    if telegram is None:
        telegram_schema: TelegramCreate = TelegramCreate(id_user=int(user_id))
        telegram = create_telegram(telegram=telegram_schema)
    telegram_hash = telegram.unique_hash_code
    return f"https://telegram.me/{settings.TELEGRAM_BOT}?start={telegram_hash}"
