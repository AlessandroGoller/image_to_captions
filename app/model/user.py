""" Module Model User """
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.dependency import database


class User(database):
    """Class for User Model"""

    __tablename__ = "t_user"
    # TODO (ale goller): maybe define init to fix error?
    user_id = Column("id_t_user", Integer, nullable=False, primary_key=True)
    email = Column("email", String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    last_access = Column(
        "last_access",
        DateTime(timezone=True),
        onupdate=func.now(),
        server_default=func.now(),
        nullable=True,
    )
    time_created = Column(
        "time_created",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
