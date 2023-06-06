""" Module Model User """
from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.dependency import database

# from sqlalchemy.orm import relationship


class User(database):
    """Class for User Model"""

    __tablename__ = "t_user"
    user_id = Column("id_t_user", Integer, nullable=False, primary_key=True)
    email = Column("email", String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    language = Column(String, nullable=True, default= "Italian")
    last_access = Column(
        "last_access",
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )
    time_created = Column(
        "time_created",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )
    email_confirmed = Column(
        "email_confirmed",
        Boolean,
        default=False
    )

    # CAUSA ERRORE
    # posts_creation = relationship("PostCreation", back_populates="User")

    def update_last_access(self) -> None:
        """ Permit to update the last acces """
        self.last_access = func.now()
