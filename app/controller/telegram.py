""" Telegram API """

from aiogram import Dispatcher, Bot, types
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.utils.logger import configure_logger
from app.dependency import get_settings
from app.schema.telegram import TelegramMessage
import time
from app.main_fastapi import dp,bot

logger = configure_logger()
settings = get_settings()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.get("")
def hello()-> dict[str,str]:
    """ Only for test """
    return {"message": "Hello, world!"}

@dp.message_handler(commands=['start'])
async def start(message: types.Message)->None:
    """ Penso al comando start """
    await message.answer(f"Salom, {message.from_user.full_name}")

@dp.message_handler()
async def main_handler(message: types.Message):
    try:
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logger.info(f'Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}')
        await message.reply(f"Hello world!{user_id=}\n{user_full_name=}\n")
    except:
        logger.info(f'Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}. Error in main_handler')
        await message.reply("Something went wrong...")   

@router.post("/webhook")
async def bot_webhook(update: dict):
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)

@router.post("/web_old")
async def telegram_webhook(message: TelegramMessage)->dict[str,str]:
    """ Telegram webhook """
    # Gestisci il messaggio qui
    # Puoi accedere al testo del messaggio con `message.text`

    # Esempio di risposta
    chat_id = message.chat.id_chat
    response_text = f'Ciao, sono un bot Telegram!\n{message.text}'
    logger.info(f"Telegram message, {chat_id=} -> {message.text=}")
    await telegram_bot.send_message(chat_id, response_text)
    return {"status": "success"}
