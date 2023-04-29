""" Module for crud for Instagram """
from typing import Optional

from sqlalchemy.orm import Session

from app.dependency import get_db
from app.model.instagram import Instagram
from app.schema.instagram import InstagramCreate, InstagramInfoBase


def get_instagram_by_id(id_instagram: int) -> Optional[Instagram]:
    """Return the Instagram from id_instagram"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.id_instagram == id_instagram).first()  # type: ignore

def get_instagram_by_user_id(user_id: int) -> Optional[list[Instagram]]:
    """Return the list of Instagram from user_id"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.id_user == user_id).all()  # type: ignore

def get_instagram_by_company_id(company_id: int) -> Optional[list[Instagram]]:
    """Return the list of Instagram from company_id"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.id_company == company_id).all()  # type: ignore

def create_instagram(instagram: InstagramCreate) -> Optional[Instagram]:
    """Creation a instagram, in input the schema of instagram create and return the instagram"""
    db: Session = next(get_db())
    db_instagram = Instagram(
        post=instagram.post,
        id_user=instagram.id_user,
        id_company = instagram.id_company,
        image_description = instagram.image_description,
        hashtags = instagram.hashtags,
        mentions = instagram.mentions,
        tagged_users = instagram.tagged_users,
        likes = instagram.likes,
        comments = instagram.comments,
        date = instagram.date,
        location = instagram.location,
        typename = instagram.typename,
        mediacount = instagram.mediacount,
        title = instagram.title,
        posturl = instagram.posturl,
    )
    db.add(db_instagram)
    db.commit()
    db.refresh(db_instagram)
    return db_instagram


def update_instagram(
    instagram: Instagram, instagram_edit: InstagramInfoBase
) -> Optional[Instagram]:
    """Permit to edit info inside instagram model"""
    db: Session = next(get_db())
    instagram_data = instagram_edit.dict(exclude_unset=True)
    for key, value in instagram_data.items():
        setattr(instagram, key, value)
    db.merge(instagram)
    db.commit()
    return instagram


def delete_instagram(instagram: Instagram) -> dict[str, bool]:
    """ Permit to delete a instagram"""
    db: Session = next(get_db())
    db.delete(instagram)
    db.commit()
    return {"ok": True}
