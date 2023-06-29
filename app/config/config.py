"""Module with all config"""

import os
from typing import Optional

from dotenv import load_dotenv
from password_strength import PasswordPolicy
from pydantic import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Class with the config"""
    APP_NAME: str = "Instapost"
    # Database config variables
    SQLALCHEMY_DATABASE_URI:str = (
        os.getenv("SQLALCHEMY_DATABASE_URI")
        or
        "sqlite:///./sql_app.db"
    )
    LANGUAGE: str = os.getenv("LANGUAGE") or "italian"
    PORT:str = os.getenv("PORT") or "5000"
    HUGGINGFACEHUB_API_TOKEN:Optional[str] = os.getenv("HUGGINGFACEHUB_API_TOKEN") or None
    OPENAI_API_TOKEN:Optional[str] = os.getenv("OPENAI_API_TOKEN") or None
    SERPAPI_API_KEY:Optional[str] = os.getenv("SERPAPI_API_KEY") or None
    REPLICATE_API_KEY:Optional[str] = os.getenv("REPLICATE_API_KEY") or None
    MODEL_BLIP:Optional[str] = (os.getenv("MODEL_BLIP") or
        "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608") # noqa
    USERNAME_IG:Optional[str] = os.getenv("USERNAME_IG") or None
    PSW_IG:Optional[str] = os.getenv("PSW_IG") or None
    TELEGRAM_TOKEN:Optional[str] = os.getenv("TELEGRAM_TOKEN") or None
    TELEGRAM_BOT: str = "images_to_caption_bot"
    WEBHOOK_PATH:str = "telegram/webhook"
    DOMAIN: str = "https://image-test-fjhr.onrender.com/"
    DOMAIN_old:str = "https://image-to-caption.onrender.com/"

policy = PasswordPolicy.from_names(
    length=8,  # min length: 8
    uppercase=2,  # need min. 2 uppercase letters
    numbers=2,  # need min. 2 digits
    special=2,  # need min. 2 special characters
    nonletters=2,  # need min. 2 non-letter characters (digits, specials, anything)
)
