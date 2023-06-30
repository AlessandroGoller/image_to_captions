""" User API """
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from app.dependency import get_settings
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(prefix="/user", tags=["home"])


@router.get("")
async def home(token: Annotated[str, Depends(oauth2_scheme)]) -> dict[str, str]:
    """Only for test"""
    return {"token": token}
