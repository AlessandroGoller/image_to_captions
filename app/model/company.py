""" Module Model Company """
from sqlalchemy import Column, Integer, String, Text

from app.dependency import database


class Company(database):
    """ Class for Company Model """
    __tablename__ = "t_company"

    id_company = Column("id_t_company", Integer, nullable=False, primary_key=True)
    name = Column("name", String, nullable=False, unique=True)
    id_user = Column(Integer, nullable=False)
    id_instagram = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    website = Column(String, nullable= True)
