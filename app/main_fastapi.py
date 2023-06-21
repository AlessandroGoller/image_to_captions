
import uvicorn

from app.app_creator import router, create_app
from app.utils.logger import configure_logger
from app.dependency import get_settings
from aiogram import types, Dispatcher, Bot

logger = configure_logger()
settings = get_settings()

app = create_app()
app.include_router(router)

# Telegram settings
### SET TELEGRAM
WEBHOOK_URL = settings.DOMAIN + settings.WEBHOOK_PATH
bot = Bot(token=settings.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
# telegram_bot.setWebhook("YOUR WEB SERVER LINK HERE" + "YOUR TOKEN HERE")

@app.on_event("startup")
async def on_startup()->None:
    """ Setting on startup """
    webhook_info = await bot.get_webhook_info()
    if webhook_info.url != WEBHOOK_URL:
        await bot.set_webhook(
            url=WEBHOOK_URL
        )

@app.on_event("shutdown")
async def on_shutdown()-> None:
    """ Settings on shutdown """
    await bot.session.close()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
