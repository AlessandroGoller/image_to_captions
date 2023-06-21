""" Necessary info for Fastapi """

from fastapi import APIRouter, FastAPI

from app.controller import telegram
from app.dependency import get_settings

settings = get_settings()

router = APIRouter()
router.include_router(telegram.router)

def create_app() -> FastAPI:
    """ Create FastApi """
    app = FastAPI()
    return app
