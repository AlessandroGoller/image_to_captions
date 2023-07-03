""" Module for User Schema """

from pydantic import BaseModel


class Token(BaseModel):
    """ Token Class """

    access_token: str
    token_type: str


class UserInfoBase(BaseModel):
    """Class UserInfoBase"""

    name: str
    email: str


class UserCreate(UserInfoBase):
    """
    Class UserCreate
    Use it during creation
    """

    password: str


class UserInfo(UserInfoBase):
    """
    Class UserInfo
    Use it during retrieving information
    """

    user_id: int

    class Config:
        """Config"""

        orm_mode = True


class UserInfoAdmin(UserInfoBase):
    """Class UserInfoAdmin"""

    user_id: int
    admin: bool

    class Config:
        """Config"""

        orm_mode = True
