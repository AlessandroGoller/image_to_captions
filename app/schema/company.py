""" Module for Company Schema """

from typing import Optional

from pydantic import BaseModel


class CompanyInfoBase(BaseModel):
    """Class CompanyInfo"""

    name: str
    url_instagram: Optional[str] = None
    description: Optional[str] = None
    website: Optional[str] = None


class CompanyCreate(CompanyInfoBase):
    """
    Class CompanyCreate
    Use it during creation
    """

    id_user: int
