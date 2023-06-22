""" Telegram """

import time
from typing import Optional

from aiogram import Bot, Dispatcher, types

from app.crud.telegram import create_telegram, delete_telegram, get_telegram_by_chat_id, update_last_access
from app.crud.user import get_user_by_hash
from app.dependency import get_settings
from app.model.user import User
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
    try:
        hash_code: str = message.text.split(" ")[1]
    except:
        await message.answer(f"Error hash code, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}")
        return "ok"
    user: Optional[User] = get_user_by_hash(hash_code=hash_code)
    if user is None:
        await message.answer(f"Salom, {message.from_user.full_name}\n \
                            Impossible to find account, try again")
        return "ok, but with impossible account"
    telegram = get_telegram_by_chat_id(message.chat.id)
    if telegram is not None:
        if telegram.id_user == user.user_id:
            update_last_access(telegram)
            await message.answer(f"Salom another time, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}\n{telegram.user.email}")
            return "ok"
        delete_telegram(telegram)
    telegram_schema = TelegramCreate(
        id_user=user.user_id,
        id_user_telegram=int(message.from_user.id),
        id_chat=int(message.chat.id)
    )
    telegram = create_telegram(telegram=telegram_schema)
    update_last_access(telegram)
    await message.answer(f"Salom, {message.from_user.full_name}\n{message.text=}\n\
                        {message.chat.id=}\n{telegram.user.email}")
    await message.answer(f"Telegram schema created:, {telegram_schema.id_user}\n{telegram_schema.id_chat=}\n\
                        {telegram_schema.id_user_telegram=}\n\nTelegram row\
                        {telegram.user.email}")
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
