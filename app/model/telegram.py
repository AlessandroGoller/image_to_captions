""" Model for telegram """

from random import getrandbits

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.dependency import database


def _createhash()->str:
    """This function generate long hash"""
    return str(getrandbits(128))

class Telegram(database):
    """Class for Telegram Model"""

    __tablename__ = "t_telegram"
    id_telegram = Column("id_t_telegram", Integer, nullable=False, primary_key=True)
    id_user = Column(Integer, ForeignKey("t_user.id_t_user"), nullable=False)
    id_chat = Column(String, nullable=True, default=None)
    unique_hash_code = Column(String, nullable=True, default=_createhash(), unique=True)
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

    def update_last_access(self) -> None:
        """ Permit to update the last acces """
        self.last_access = func.now()
