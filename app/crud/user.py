""" Module for crud for Users """

from typing import Optional

import bcrypt
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.model.user import User
from app.schema.user import UserCreate


def get_user_by_email(email: Optional[str]) -> Optional[User]:
    """ return user from email """
    db:Session = next(get_db())
    return db.query(User).filter(User.email == email).first()  # type: ignore

def get_user_by_id(user_id: str) -> Optional[User]:
    """ Return the user from user_id """
    db:Session = next(get_db())
    return db.query(User).filter(User.user_id == user_id).first()  # type: ignore

def get_users() -> Optional[list[User]]:
    """ Return the list of users """
    db:Session = next(get_db())
    db_users = db.query(User).all()
    return db_users # type: ignore

def create_user(user: UserCreate) -> Optional[User]:
    """ Creation a user, in input the schema of user create and return the user"""
    db:Session = next(get_db())
    hashed_password = bcrypt.hashpw(user.password.encode("utf-8"), bcrypt.gensalt()).decode('utf8')
    db_user = User(email=user.email, password=hashed_password, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def become_admin(email: str) -> Optional[User]:
    """ Convert a user to admin """
    db:Session = next(get_db())
    user = get_user_by_email(email=email)
    if user is None:
        return None
    user.admin = True
    db.commit()
    db.refresh(user)
    return user
