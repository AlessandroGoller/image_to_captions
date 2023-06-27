"""
Module for start FastApi
"""
from app.app_creator import create_app, router
from app.dependency import get_settings
from app.services.telegram_bot import WEBHOOK_URL, bot, commands
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

app = create_app()
app.include_router(router)


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
