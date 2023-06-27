""" Module with utils regarding prompt Optimization """

from typing import Optional

from app.model.instagram import Instagram
from app.utils.openai.tokenization import limit_posts_for_token


def create_prompt(
    sample_posts: Optional[list[Instagram]], image_description: str
) -> str:
    """
    create and return the prompt

    Parameters
    ----------
    sample_posts : list[Instagram]
    image_description : str

    Returns
    -------
    str
    """
    prompt: str = limit_posts_for_token(sample_posts)
    prompt += (
        ". Personalizza il post perchè sia adatto ad un'immagine di "
        + image_description
        + ". Inserisci emoticons e hashtags nel post. Attieniti al formato degli esempi."
    )  # noqa
    return prompt
