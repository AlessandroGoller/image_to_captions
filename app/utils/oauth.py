""" Module for auth """
import time
from datetime import datetime, timedelta
from typing import Annotated, Optional, Union

import bcrypt  # noqa: I001
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.crud.user import create_user, get_user_by_email
from app.dependency import get_settings
from app.model.user import User
from app.schema.user import UserCreate, UserInfoBase
from app.utils.logger import configure_logger

logger = configure_logger()
settings = get_settings()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.TOKEN_URL)

SECRET_KEY = settings.SECRET_KEY_JWT
ALGORITHM = settings.ALGORITHM_JWT
ACCESS_TOKEN_EXPIRE_MINUTES = int(settings.ACCESS_TOKEN_EXPIRE_MINUTES)
TIME_FOR_WRONG_LOGIN = 0.5

def protect_timing_attack(start_time: float)->None:
    """
    If wrong username or password wait some time.
    This method should protect against timing attack

    Parameters
    ----------
    start_time : time
    """
    end_time = time.time()
    time_to_wait = TIME_FOR_WRONG_LOGIN-end_time-start_time
    if time_to_wait > 0:
        time.sleep(time_to_wait)

def verify_login(email: str, password: str) -> bool:
    """
    Verifica se l'utente con username e password esiste nella lista degli utenti registrati
    e se le credenziali sono corrette.
    """
    start_time = time.time()
    email = email.strip()
    user = get_user_by_email(email=email)
    if user is None:
        protect_timing_attack(start_time)
        return False
    stored_password = user.password

    check_psw = bool(
        bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8"))
    )
    if check_psw:
        return True

    protect_timing_attack(start_time)
    return False

def register_user(email: str, password: str) -> bool:
    """
    Registra un nuovo utente con email e password.
    Restituisce True se la registrazione è andata a buon fine,
    False se l'username è già stato utilizzato.
    """
    email = email.strip()
    user = get_user_by_email(email=email)
    if user is not None:
        return False
    data = UserCreate(name="Noname", email=email, password=password)
    user = create_user(user=data)
    if user is None:
        return False
    return True

async def return_current_user(token: Annotated[str, Depends(oauth2_scheme)])->UserInfoBase:
    """ From the token passed, check if it is valid and if true return the user """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError as exc:
        logger.error(exc)
        raise credentials_exception from exc
    user: Optional[User] = get_user_by_email(email=username)
    if user is None:
        raise credentials_exception
    return UserInfoBase(
        email=user.email,
        name=user.name
    )

def create_access_token(
        data: dict,
        expires_delta: Union[timedelta, None] = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )->str:
    """ Create the token to return """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
