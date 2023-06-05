""" Module Model Post Creation """
from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, LargeBinary, String, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.dependency import database


class PostCreation(database):
    """Class for PostCreation Model"""

    __tablename__ = "t_post_creation"

    id_post_creation = Column("id_t_post_creation", Integer, nullable=False, primary_key=True)
    user_id = Column("id_t_user", Integer, ForeignKey("t_user.id_t_user"), nullable=False)
    image_uploaded = Column("image_uploaded", LargeBinary, nullable=True)
    description = Column("Description", String, nullable=True)
    prompt = Column("prompt", Text, nullable=True)
    post_created = Column("post_created", Text, nullable=True)
    refinement = Column("refinement", JSON, nullable=True)
    time_created = Column( # pylint: disable=R0801
        "time_created",
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=True,
    )

    user = relationship("User", uselist=False)
