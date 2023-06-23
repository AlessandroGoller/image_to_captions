""" Model for telegram """

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.dependency import database


class Telegram(database):
    """Class for Telegram Model"""

    __tablename__ = "t_telegram"
    id_telegram = Column("id_t_telegram", Integer, nullable=False, primary_key=True)
    id_user = Column(Integer, ForeignKey("t_user.id_t_user"), nullable=False)
    id_user_telegram = Column(Integer, nullable=True, default=None)
    id_chat = Column(Integer, nullable=True, default=None, unique=True)
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
    # save the message id where we can find the value
    message_id_image = Column(Integer, nullable=True, default=None)
    message_id_description = Column(Integer, nullable=True, default=None)
    message_id_prompt = Column(Integer, nullable=True, default=None)

    user = relationship("User", uselist=False, lazy="joined")

    def update_last_access(self) -> None:
        """ Permit to update the last acces """
        self.last_access = func.now()
