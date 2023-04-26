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
