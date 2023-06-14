""" Module Model Company """
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.dependency import database


class Company(database):
    """Class for Company Model"""

    __tablename__ = "t_company"

    id_company = Column("id_t_company", Integer, nullable=False, primary_key=True)
    name = Column("name", String, nullable=False)
    id_user = Column(Integer, ForeignKey("t_user.id_t_user"), nullable=False)
    url_instagram = Column(String, nullable=True)
    language = Column(String, nullable=True, default= "Auto")
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)
    tokens_to_be_paid = Column("tokens_to_be_paid", Integer, nullable=True, default=0)
    total_tokens = Column("total_tokens", Integer, nullable=True, default=0)
    profile_pic_url = Column("profile_pic_url", String, nullable=True, default=None)

    user = relationship("User", uselist=False)
