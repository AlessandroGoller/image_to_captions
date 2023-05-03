"""Module with all config"""

import os
from typing import Optional

from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """Class with the config"""
    # Database config variables
    SQLALCHEMY_DATABASE_URI:str = (
        os.getenv("SQLALCHEMY_DATABASE_URI")
        or
        "sqlite:///./sql_app.db"
    )

    LANGUAGE:str = os.getenv("LANGUAGE") or "italian"
    PORT:str = os.getenv("PORT") or "5000"
    HUGGINGFACEHUB_API_TOKEN:Optional[str] = os.getenv("HUGGINGFACEHUB_API_TOKEN") or None
    OPENAI_API_TOKEN:Optional[str] = os.getenv("OPENAI_API_TOKEN") or None
    SERPAPI_API_KEY:Optional[str] = os.getenv("SERPAPI_API_KEY") or None
    REPLICATE_API_KEY:Optional[str] = os.getenv("REPLICATE_API_KEY") or None
    MODEL_BLIP:Optional[str] = (os.getenv("MODEL_BLIP") or
        "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608") # noqa
