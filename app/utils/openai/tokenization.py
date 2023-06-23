""" Module with utils regarding tokenization """

import tiktoken
from typing import Optional

from app.crud.company import add_tokens, get_company_by_user_id
from app.crud.user import get_user_by_email
from app.model.instagram import Instagram
from app.utils.logger import configure_logger

logger = configure_logger()

def num_tokens_from_messages(messages:list, model:str="gpt-3.5-turbo-0301")->int:
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo":
        print("Warning: gpt-3.5-turbo may change over time. Returning num tokens assuming gpt-3.5-turbo-0301.")
        return num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301")
    elif model == "gpt-4":
        print("Warning: gpt-4 may change over time. Returning num tokens assuming gpt-4-0314.")
        return num_tokens_from_messages(messages, model="gpt-4-0314")
    elif model == "gpt-3.5-turbo-0301":
        tokens_per_message = 4  # every message follows <|start|>{role/name}\n{content}<|end|>\n
        tokens_per_name = -1  # if there's a name, the role is omitted
    elif model == "gpt-4-0314":
        tokens_per_message = 3
        tokens_per_name = 1
    else:
        raise NotImplementedError(f"""num_tokens_from_messages() is not implemented for model {model}.""")
    num_tokens = 0
    for message in messages:
        num_tokens += tokens_per_message
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":
                num_tokens += tokens_per_name
    num_tokens += 3  # every reply is primed with <|start|>assistant<|message|>
    return num_tokens

def num_tokens_from_string(string:str, model:str="gpt-3.5-turbo-0301")->int:
    """Returns the number of tokens used by a string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        print("Warning: model not found. Using cl100k_base encoding.")
        encoding = tiktoken.get_encoding("cl100k_base")

    num_tokens = 0
    num_tokens += len(encoding.encode(string))

    return num_tokens

def add_tokens_to_db(string:str, email:str)->None:
    """ Insert token inside db """
    user = get_user_by_email(email=email)
    if user is None:
        logger.error("Profile Page without having an account")
        raise ValueError("Impossible Position")
    company = get_company_by_user_id(user_id=user.user_id)
    if company is None:
        logger.error("Try to insert token without having a company")
        raise ValueError("Impossible Position")
    tokens = num_tokens_from_string(string)
    _,_ = add_tokens(company=company, tokens=tokens)

def limit_posts_for_token(sample_posts:Optional[list[Instagram]])->str:
    """
    limit_posts_for_token
    Return the prompt with instagram posts, limited by token

    Parameters
    ----------
    sample_posts : list[Instagram]

    Returns
    -------
    str
    """
    # To be sure, we will add each post until we reach 3500 tokens maximum
    if sample_posts is None:
        raise ValueError("No posts found")
    tok = 0
    posts = 0
    prompt = "Genera un post per instagram, seguendo il formato degli esempi che fornisco:" # noqa
    for example in sample_posts:
        # We insert posts until we reach 3500 tokens
        # QUEST: are the post in order from the most recent?
        if (tok+num_tokens_from_string(example.post)<3500):
            prompt += ' "' + str(example.post) + '",'
            tok += num_tokens_from_string(example.post)
            posts += 1
        else:
            break
    logger.info(f"Inserted {posts} post, corresponding to {tok} tokens, in the prompt")
    prompt = prompt[:-1] # Remove the comma
    return prompt


if __name__=="__main__":
    messages = [{"role": "user", "content": "Hello, world!"}, {"role": "assistant", "content": "Hello, world!"}]
    print(num_tokens_from_messages(messages, model="gpt-3.5-turbo"))
    string = "Hello, world! here all good"
    print(num_tokens_from_string(string, model="gpt-3.5-turbo"))
