""" Streamlit helper profile """

import traceback
from io import BytesIO
from typing import Optional

import requests
from PIL import Image

from app.crud.company import add_profile_pic
from app.dependency import get_settings
from app.model.company import Company
from app.services.ig_scraping import GetInstagramProfile
from app.utils.logger import configure_logger

settings = get_settings()

logger = configure_logger()

def request_image_from_url(url_pic:str)->Optional[BytesIO]:
    """
    request_image_from_url

    Parameters
    ----------
    url_pic : str

    Returns
    -------
    Optional[BytesIO]
    """
    if url_pic is None:
        logger.warning("Error, None as url_pic") # type: ignore
        return None
    try:
        logger.info(f"Request on {url_pic=}")
        response = requests.get(url_pic, timeout=20)
        image = Image.open(BytesIO(response.content))
        return image # type: ignore
    except Exception as error:
        traceback_msg = traceback.format_exc()
        logger.error(f"Impossible to request the profile pic\n{error}\n{traceback_msg}")
    return None

def get_profile_pic(company:Company)->Optional[BytesIO]:
    """
    get_profile_pic of the instagram account

    Parameters
    ----------
    company : Company

    Returns
    -------
    BytesIO
    """
    url_pic: str = company.profile_pic_url
    if url_pic is not None:
        image:Optional[BytesIO] = request_image_from_url(url_pic)
        if image is not None:
            return image
    try:
        client = GetInstagramProfile()
        url_pic = client.get_profile_url(company.url_instagram)
    except Exception as error:
        traceback_msg = traceback.format_exc()
        logger.warning(f"Impossible showing the profile pic\n{error}\n{traceback_msg}")
    add_profile_pic(company=company, url_pic=url_pic)
    image = request_image_from_url(url_pic)
    if image is not None:
        return image
    return None
