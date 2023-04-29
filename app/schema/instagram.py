""" Module for Instagram Schema """

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class InstagramInfoBase(BaseModel):
    """Class InstagramInfo"""

    post: Optional[str] = None
    image_description: Optional[str] = None
    hashtags: Optional[str] = None
    mentions: Optional[str] = None
    tagged_users: Optional[str] = None
    likes: Optional[int] = None
    comments: Optional[int] = None
    date: Optional[datetime] = None
    location: Optional[str] = None
    typename: Optional[str] = None
    mediacount: Optional[int] = None
    title: Optional[str] = None
    posturl: Optional[str] = None


class InstagramCreate(InstagramInfoBase):
    """
    Class InstagramCreate
    Use it during creation
    """

    id_company: int
    id_user: int
