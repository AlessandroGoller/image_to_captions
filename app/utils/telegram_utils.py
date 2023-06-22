""" Help function for telegram """

from typing import Literal, Optional, Union

from memoization import cached

from app.crud.telegram import get_telegram_by_chat_id, update_last_access
from app.dependency import get_settings
from app.model.telegram import Telegram
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()


@cached(max_size=32, ttl=30)
def check_chat(id_chat: int)->Union[Literal[False],Telegram]:
    """
    check if the message arrive from an authorize user or not.
    If is invalid return False.
    If is Valid return the telegram Model

    Parameters
    ----------
    id_chat : int

    Returns
    -------
    Union[bool,Telegram]
    """
    telegram:Optional[Telegram] = get_telegram_by_chat_id(id_chat)
    if telegram is None:
        return False
    update_last_access(telegram.id_telegram)
    return telegram
