""" Telegram API """

from aiogram import Bot, Dispatcher, types
from fastapi import APIRouter

from app.dependency import get_settings
from app.services.telegram_bot import bot, dp
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

router = APIRouter(prefix="/telegram", tags=["telegram"])

@router.get("")
def hello()-> dict[str,str]:
    """ Only for test """
    return {"message": "Hello, world!"}

@router.post("/webhook")
async def telegram_webhook(update: dict)->str:
    """ Telegram webhook """
    telegram_update = types.Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    await dp.process_update(telegram_update)
    return "ok"
