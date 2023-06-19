""" Module for Telegram Schema """

from typing import Optional

from pydantic import BaseModel


class TelegramInfoBase(BaseModel):
    """Class TelegramInfo"""

class TelegramCreate(TelegramInfoBase):
    """
    Class TelegramCreate
    Use it during creation
    """
    id_user: int

class Chat(BaseModel):
    """ Classe for """
    id_chat: int
    # Altri campi della chat, se necessario

class TelegramMessage(BaseModel):
    """ How the Telegram Message is composed """
    # Definisci i campi del messaggio che desideri gestire
    chat: Chat
    text: str
    # Altri campi del messaggio, se necessario
