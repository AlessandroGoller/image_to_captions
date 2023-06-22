""" Help function for telegram """

from typing import Literal, Optional, Union

from aiogram import types

from app.crud.telegram import get_telegram_by_chat_id, update_last_access
from app.dependency import get_settings
from app.model.telegram import Telegram
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

def check_chat(message: types.Message)->Union[Literal[False],Telegram]:
    """
    check if the message arrive from an authorize user or not.
    If is invalid return False.
    If is Valid return the telegram Model

    Parameters
    ----------
    message : types.Message

    Returns
    -------
    Union[bool,Telegram]
    """
    telegram:Optional[Telegram] = get_telegram_by_chat_id(message.chat.id)
    if telegram is None:
        return False
    update_last_access(telegram.id_telegram)
    return telegram
