""" Module for crud for Post Creation """
from typing import Optional

from sqlalchemy.orm import Session

from app.dependency import get_db
from app.model.post_creation import PostCreation
from app.schema.post_creation import PostCreationCreate
from app.utils.logger import configure_logger

logger = configure_logger()


def get_post_creation_by_id(id_post_creation: int) -> Optional[PostCreation]:
    """Return the PostCreation from id_company"""
    db: Session = next(get_db())
    return db.query(PostCreation).filter(PostCreation.id_post_creation == id_post_creation).first()  # type: ignore


def update_refinement() -> None:
    """Add refinement to the json"""
    print("TODO")


def create_post_creation(post_creation: PostCreationCreate) -> Optional[PostCreation]:
    """Creation a post, in input the schema of post create and return the post"""
    db: Session = next(get_db())
    db_post_creation = PostCreation(
        description=post_creation.description,
        user_id=post_creation.user_id,
        prompt=post_creation.prompt,
        posts_created=(
            ";-;".join(post_creation.posts_created)
            if isinstance(post_creation.posts_created, list)
            else post_creation.posts_created
        ),
        image_uploaded=post_creation.image_uploaded,
    )
    db.add(db_post_creation)
    db.commit()
    db.refresh(db_post_creation)
    return db_post_creation


def delete_all_posts_creation(id_user: int) -> None:
    """Delete all post created connected to a user"""
    db: Session = next(get_db())
    # Get all PostCreation accounts connected to the user
    posts: list[PostCreation] = db.query(PostCreation).filter_by(user_id=id_user).all()
    # Delete each Instagram account
    for post in posts:
        try:
            delete_post_with_sessione(db, post)
        except Exception as error:
            logger.error(
                f"Error during deletion of the post post {post.id_post_creation}\n{error}"
            )


def delete_post_with_sessione(db: Session, post: PostCreation) -> None:
    """Permit to delete a post with an already started session"""
    db.delete(post)
    db.commit()


def delete_posts_creation(id_post_creation: int) -> None:
    """Permit to remove a post created"""
    logger.info("Delete Post Created")
    db: Session = next(get_db())
    post_creation = get_post_creation_by_id(id_post_creation=id_post_creation)
    db.delete(post_creation)
    db.commit()
