""" Module Model User """
from random import getrandbits

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.dependency import database


def _createhash()->str:
    """This function generate long hash"""
    return str(getrandbits(128))

class User(database):
    """Class for User Model"""

    __tablename__ = "t_user"
    user_id = Column("id_t_user", Integer, nullable=False, primary_key=True)
    email = Column("email", String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    language = Column(String, nullable=True, default= "Italian") # pylint: disable=R0801
    last_access = Column( # pylint: disable=R0801
        "last_access",
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )
    time_created = Column( # pylint: disable=R0801
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
    is_paid = Column("is_paid", Boolean, nullable=True, default=False)
    data_first_paid = Column("data_first_paid", DateTime(timezone=True),nullable=True)
    data_last_paid = Column("data_last_paid", DateTime(timezone=True),nullable=True)
    # we should use this like a sum of the company tokens
    tokens_to_be_paid = Column("tokens_to_be_paid", Integer, nullable=True, default=0)
    total_tokens = Column("total_tokens", Integer, nullable=True, default=0)
    unique_hash_code = Column(String, nullable=True, default=_createhash(), unique=True)


    def update_last_access(self) -> None:
        """ Permit to update the last acces """
        self.last_access = func.now()
