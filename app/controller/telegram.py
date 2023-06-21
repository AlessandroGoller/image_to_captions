""" Telegram API """

from aiogram import Dispatcher, Bot, types
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.utils.logger import configure_logger
from app.dependency import get_settings
from app.schema.telegram import TelegramMessage
from app.services.telegram_bot import dp,bot

logger = configure_logger()
settings = get_settings()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.get("")
def hello()-> dict[str,str]:
    """ Only for test """
    return {"message": "Hello, world!"}

@router.post("/webhook")
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@router.post("/web_old")
async def telegram_webhook(message: TelegramMessage)->dict[str,str]:
    """ Telegram webhook """
    return "ok, fastapi online"
    # Gestisci il messaggio qui
    # Puoi accedere al testo del messaggio con `message.text`

    # Esempio di risposta
    chat_id = message.chat.id_chat
    response_text = f'Ciao, sono un bot Telegram!\n{message.text}'
    logger.info(f"Telegram message, {chat_id=} -> {message.text=}")
    await telegram_bot.send_message(chat_id, response_text)
    return {"status": "success"}
