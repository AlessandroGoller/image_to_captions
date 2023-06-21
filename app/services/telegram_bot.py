""" Telegram """

import time
from typing import Optional

from aiogram import Bot, Dispatcher, types

from app.crud.telegram import create_telegram, get_telegram_by_user_id
from app.dependency import get_settings
from app.model.telegram import Telegram
from app.schema.telegram import TelegramCreate
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

# Telegram settings
WEBHOOK_URL = settings.DOMAIN + settings.WEBHOOK_PATH
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands="start")
async def start(message: types.Message)->str:
    """ Anwser message for commands start """
    await message.answer(f"Salom, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}\n")
    return "ok"

@dp.message_handler()
async def main_handler(message: types.Message)-> str:
    """ Anwser message for other commands """
    try:
        user_id = message.from_user.id
        user_full_name = message.from_user.full_name
        logger.info(f"Main: {user_id} {user_full_name} {time.asctime()}. Message: {message}")
        await message.reply(f"Hello world!{user_id=}\n{user_full_name=}\n")
        return "Correct Answer"
    except Exception as error:
        logger.info(f"Main: {user_id} {user_full_name} {time.asctime()}.\
                    Message: {message}. Error in main_handler\n {error}")
        await message.reply("Something went wrong...")
        return f"There was an error: {error}"

def get_telegram_url(user_id: str)->str:
    """ Return the url for telegram connection """
    telegram: Optional[Telegram] = get_telegram_by_user_id(id_user=int(user_id))
    if telegram is None:
        telegram_schema: TelegramCreate = TelegramCreate(id_user=int(user_id))
        telegram = create_telegram(telegram=telegram_schema)
    telegram_hash = telegram.unique_hash_code
    return f"https://telegram.me/{settings.TELEGRAM_BOT}?start={telegram_hash}"
