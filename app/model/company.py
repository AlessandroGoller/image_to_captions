""" Module Model Company """
from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.dependency import database


class Company(database):
    """Class for Company Model"""

    __tablename__ = "t_company"

    id_company = Column("id_t_company", Integer, nullable=False, primary_key=True)
    name = Column("name", String, nullable=False, unique=True)
    id_user = Column(Integer, ForeignKey("t_user.id_t_user"), nullable=False)
    url_instagram = Column(String, nullable=True)
    language = Column(String, nullable=True, default= "Auto")
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)

    user = relationship("User", uselist=False)
