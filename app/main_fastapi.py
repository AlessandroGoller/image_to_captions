"""
Module for start FastApi
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controller import telegram
from app.dependency import get_settings
from app.services.telegram_bot import WEBHOOK_URL, bot, commands
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()


app = FastAPI(title=settings.APP_NAME)
app.include_router(telegram.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def on_startup() -> None:
    """Setting on startup"""
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL,
            drop_pending_updates=True,
        )
    await bot.set_my_commands(commands)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """Settings on shutdown"""
    await bot.session.close()
