""" Module for crud for Instagram """
import traceback
from datetime import datetime
from typing import Optional

from memoization import cached
from sqlalchemy.orm import Session

from app.dependency import get_db
from app.model.instagram import Instagram
from app.schema.instagram import InstagramCreate, InstagramInfoBase
from app.utils.logger import configure_logger

logger = configure_logger()


def get_instagram_by_id(id_instagram: int) -> Optional[Instagram]:
    """Return the Instagram from id_instagram"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.id_instagram == id_instagram).first()


def get_instagram_by_url(url: int) -> Optional[Instagram]:
    """Return the Instagram from url"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.posturl == url).first()


def get_instagram_by_user_id(user_id: int) -> Optional[list[Instagram]]:
    """Return the list of Instagram from user_id"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.id_user == user_id).all()


def get_instagram_by_company_id(company_id: int) -> Optional[list[Instagram]]:
    """Return the list of Instagram from company_id"""
    db: Session = next(get_db())
    return db.query(Instagram).filter(Instagram.id_company == company_id).all()


@cached(max_size=16, ttl=300)
def get_last_n_instagram(
    company_id: int, number_ig: int = 20
) -> Optional[list[Instagram]]:
    """Return the list of n Instagram from company_id order by date"""
    db: Session = next(get_db())
    return (
        db.query(Instagram)
        .filter(Instagram.id_company == company_id)
        .order_by(Instagram.date.desc())
        .limit(number_ig)
        .all()
    )


def get_instagram_after_date(
    company_id: int, date: datetime
) -> Optional[list[Instagram]]:
    """Return the list of Instagram posts from company_id with date after the input date"""
    db: Session = next(get_db())
    return (
        db.query(Instagram)
        .filter(Instagram.id_company == company_id, Instagram.date > date)
        .all()
    )


def create_instagram(instagram: InstagramCreate) -> Optional[Instagram]:
    """Creation a instagram, in input the schema of instagram create and return the instagram"""
    db: Session = next(get_db())
    db_instagram = Instagram(
        post=instagram.post,
        id_user=instagram.id_user,
        id_company=instagram.id_company,
        image_description=instagram.image_description,
        hashtags=instagram.hashtags,
        mentions=instagram.mentions,
        tagged_users=instagram.tagged_users,
        likes=instagram.likes,
        comments=instagram.comments,
        date=instagram.date,
        location=instagram.location,
        typename=instagram.typename,
        mediacount=instagram.mediacount,
        title=instagram.title,
        posturl=instagram.posturl,
    )
    db.add(db_instagram)
    db.commit()
    db.refresh(db_instagram)
    logger.info(f"Inserted IG post on db, {instagram.posturl=}")
    return db_instagram


def bulk_create_instagram(instagrams: list[InstagramCreate]) -> None:
    """Bulk creation of instagrams"""
    db: Session = next(get_db())
    db_instagrams = []

    # Create a set of unique post URLs
    unique_urls = {instagram.posturl for instagram in instagrams}

    # Retrieve Instagrams from the database for the unique post URLs
    existing_instagrams = (
        db.query(Instagram).filter(Instagram.posturl.in_(unique_urls)).all()
    )
    existing_instagram_urls = {instagram.posturl for instagram in existing_instagrams}

    # Create Instagram objects for any new URLs
    for instagram in instagrams:
        # Future Todo: it doesn't check if two user or two company use the same account
        # Think about it
        if instagram.posturl not in existing_instagram_urls:
            try:
                db_instagrams.append(
                    Instagram(
                        post=instagram.post,
                        id_user=instagram.id_user,
                        id_company=instagram.id_company,
                        image_description=instagram.image_description,
                        hashtags=instagram.hashtags,
                        mentions=instagram.mentions,
                        tagged_users=instagram.tagged_users,
                        likes=instagram.likes,
                        comments=instagram.comments,
                        date=instagram.date,
                        location=instagram.location,
                        typename=instagram.typename,
                        mediacount=instagram.mediacount,
                        title=instagram.title,
                        posturl=instagram.posturl,
                    )
                )
            except Exception as error:
                logger.error(
                    f"Probably tried to insert an already present data\n{error}\n{traceback}"
                )
                return None
    logger.info("Finish converted data to instagram schema")

    if db_instagrams:
        db.add_all(db_instagrams)
        db.commit()

        # Refresh each instance of the model individually
        for db_instagram in db_instagrams:
            db.refresh(db_instagram)
        logger.info(f"New {len(db_instagrams)} data Inserted")
        return None

    logger.info("No new data Inserted")
    return None


def insert_data_to_db(data: dict, user_id: int, company_id: int) -> bool:
    """From a dict of data, insert everythin inside Instagram db"""
    try:
        instagrams = [
            InstagramCreate(
                post=post.get("post"),
                id_user=user_id,
                id_company=company_id,
                image_description=post.get("image_description", None),
                hashtags=";".join(post.get("hashtags", None)),
                mentions=";".join(post.get("mentions", None)),
                tagged_users=";".join(post.get("tagged_users", None)),
                likes=post.get("likes", None),
                comments=post.get("comments", None),
                date=post.get("date", None),
                location=post.get("location", None),
                typename=post.get("typename", None),
                mediacount=post.get("mediacount", None),
                title=post.get("title", None),
                posturl=post.get("posturl", None),
            )
            for post in data.values()
        ]
        bulk_create_instagram(instagrams)
        return True

    except Exception as error:
        logger.error(
            f"Error during insertion bunch of data inside db Instagram\n{error=}\n{traceback}"
        )
        return False


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


def delete_all_instagram(id_company: int) -> None:
    """Delete all instagram account connected to a company"""
    db: Session = next(get_db())
    # Get all Instagram accounts connected to the company
    instagrams: list[Instagram] = (
        db.query(Instagram).filter_by(id_company=id_company).all()
    )
    # Delete each Instagram account
    for instagram in instagrams:
        try:
            delete_instagram_with_sessione(db, instagram)
        except Exception as error:
            logger.error(
                f"Error during deletion of the instagram post {instagram.posturl}\n{error}"
            )


def delete_instagram_with_sessione(db: Session, instagram: Instagram) -> None:
    """Permit to delete a instagram with an already started session"""
    db.delete(instagram)  # type: ignore
    db.commit()


def delete_instagram(instagram: Instagram) -> dict[str, bool]:
    """Permit to delete a instagram"""
    db: Session = next(get_db())
    db.delete(instagram)  # type: ignore
    db.commit()
    return {"ok": True}
