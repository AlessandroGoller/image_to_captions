""" Telegram API """

import telegram
from fastapi import APIRouter, Depends, HTTPException, status, Response

from app.utils.logger import configure_logger
from app.dependency import get_settings
from app.schema.telegram import TelegramMessage

logger = configure_logger()
settings = get_settings()

router = APIRouter(prefix="/telegram", tags=["telegram"])

telegram_bot = telegram.Bot(token=settings.TELEGRAM_TOKEN)

@router.get("")
def hello()-> dict[str,str]:
    """ Only for test """
    return {"message": "Hello, world!"}

@router.post("/webhook")
async def telegram_webhook(message: TelegramMessage)->dict[str,str]:
    """ Telegram webhook """
    # Gestisci il messaggio qui
    # Puoi accedere al testo del messaggio con `message.text`

    # Esempio di risposta
    chat_id = message.chat.id_chat
    response_text = f'Ciao, sono un bot Telegram!\n{message.text}'
    await telegram_bot.send_message(chat_id, response_text)
    return {"status": "success"}
