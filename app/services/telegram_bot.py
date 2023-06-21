""" Telegram """

from typing import Optional

from app.crud.telegram import create_telegram, get_telegram_by_user_id
from app.dependency import get_settings
from app.model.telegram import Telegram
from app.schema.telegram import TelegramCreate
from app.utils.logger import configure_logger
from aiogram import Dispatcher, Bot, types
import time

logger = configure_logger()
settings = get_settings()

# Telegram settings
### SET TELEGRAM
WEBHOOK_URL = settings.DOMAIN + settings.WEBHOOK_PATH
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
# telegram_bot.setWebhook("YOUR WEB SERVER LINK HERE" + "YOUR TOKEN HERE")

def get_telegram_url(user_id: str)->str:
    """ Return the url for telegram connection """
    telegram: Optional[Telegram] = get_telegram_by_user_id(id_user=int(user_id))
    if telegram is None:
        telegram_schema: TelegramCreate = TelegramCreate(id_user=int(user_id))
        telegram = create_telegram(telegram=telegram_schema)
    telegram_hash = telegram.unique_hash_code
    return f"https://telegram.me/{settings.TELEGRAM_BOT}?start={telegram_hash}"

@dp.message_handler(commands="start")
async def start(message: types.Message):
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