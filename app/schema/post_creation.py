""" Module for PostCreation Schema """

from typing import Optional, Union

from pydantic import BaseModel


class PostCreationInfoBase(BaseModel):
    """Class PostCreationInfo"""

    description: Optional[str] = None
    prompt: Optional[str] = None
    posts_created: Optional[Union[str, list[str]]] = None
    image_uploaded: Optional[bytes] = None

class PostCreationCreate(PostCreationInfoBase):
    """
    Class PostCreationCreate
    Use it during creation
    """

    user_id: int
