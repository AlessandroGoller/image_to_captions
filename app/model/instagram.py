""" Module Model Instagram """
from sqlalchemy import Column, DateTime, Index, Integer, String, text

from app.dependency import database


class Instagram(database):
    """Class for Instagram Model"""

    __tablename__ = "t_instagram"

    id_instagram = Column("id_t_instagram", Integer, nullable=False, primary_key=True)
    id_company = Column(Integer, nullable=False)
    id_user = Column(Integer, nullable=False)
    post = Column(String, nullable=True)
    image_description = Column(String, nullable=True)
    hashtags = Column(String, nullable=True)
    mentions = Column(String, nullable=True)
    tagged_users = Column(String, nullable=True)
    likes = Column(Integer, nullable=True)
    comments = Column(Integer, nullable=True)
    date = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    typename = Column(String, nullable=True)
    mediacount = Column(Integer, nullable=True)
    title = Column(String, nullable=True)
    posturl = Column(String, nullable=True, unique=False)

    idx_instagram_unique_cols = Index(
        "idx_instagram_unique_cols",
        id_company,
        id_user,
        post,
        image_description,
        hashtags,
        mentions,
        tagged_users,
        likes,
        comments,
        date,
        location,
        typename,
        mediacount,
        title,
        posturl,
        unique=True,
        postgresql_where=text("post IS NOT NULL"),
    )

    def __str__(self) -> str:
        """redefine strng method"""
        return f"Post: {self.post} - Hashtags: {self.hashtags}"
