from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.sql import func

from app.dependency import database


class User(database):
    __tablename__ = "t_user"

    user_id = Column("id_t_user", Integer, nullable=False, primary_key=True)
    email = Column("email", String, nullable=False, unique=True)
    name = Column(String, nullable=True)
    password = Column(String)
    admin = Column(Boolean, default=False)
    last_access = Column("last_access", DateTime(timezone=True), onupdate=func.now(), nullable=True)
    time_created = Column("time_created", DateTime(timezone=True), server_default=func.now(), nullable=True)
