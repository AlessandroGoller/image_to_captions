""" User API """
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.dependency import get_settings
from app.schema.user import Token, UserInfoBase
from app.utils.logger import configure_logger
from app.utils.oauth import create_access_token, return_current_user, verify_login

logger = configure_logger()
settings = get_settings()

router = APIRouter(prefix="/user", tags=["home"])

@router.post("/token", response_model=Token)
async def get_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
)->Token:
    """
    If username and password are correct,
    return the jwt token

    Parameters
    ----------
    form_data : Annotated[OAuth2PasswordRequestForm, Depends

    Returns
    -------
    Token
    """
    exist_user = verify_login( email=form_data.username, password=form_data.password)
    if not exist_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": form_data.username})
    return Token(access_token=access_token,
                token_type="bearer")

@router.get("/me/", response_model=UserInfoBase)
async def get_current_user(
    current_user: Annotated[UserInfoBase, Depends(return_current_user)]
)-> UserInfoBase:
    """ Return the current User """
    return current_user
