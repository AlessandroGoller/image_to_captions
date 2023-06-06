""" Module for langchain """

from io import BytesIO

import openai
import replicate
from langchain import HuggingFaceHub  # , LLMChain, PromptTemplate
from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI

from app.dependency import get_settings
from app.utils.decorators import timeit
from app.utils.logger import configure_logger

settings = get_settings()

logger = configure_logger()

@timeit
def prepare_llm(provider:str="openai") -> HuggingFaceHub:
    """Return the llm"""
    if provider=="openai":
        if settings.OPENAI_API_TOKEN is not None:
            logger.info("Using OpenAI as llm")
            llm = OpenAI(
                model_name="text-davinci-003", openai_api_key=settings.OPENAI_API_TOKEN
            )
    elif provider=="huggingfacehub":
        logger.info("Using Hugging_face as llm")
        logger.info("Remember that huggingface might not work for a lot of requests")
        if settings.HUGGINGFACEHUB_API_TOKEN is not None:
            # initialize Hub LLM
            llm = HuggingFaceHub(
                repo_id="google/flan-t5-xl",
                model_kwargs={"temperature": 0, "max_length": 512},
                huggingfacehub_api_token=settings.HUGGINGFACEHUB_API_TOKEN,
            )
    else:
        logger.error("Please specify a valid llm provider")
        raise ValueError("No llm found")
    return llm

@timeit
def search_info_of_company(name_to_search: str) -> str:
    """
    search_info_of_company
    Search on Internet for info of a company name and return them.

    Parameters
    ----------
    name_to_search : str

    Returns
    -------
    str
    """
    llm = prepare_llm()
    tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=settings.SERPAPI_API_KEY)
    agent = initialize_agent(
        tools, llm, agent="zero-shot-react-description", verbose=True
    )
    response = agent.run(
        f"What products or services does {name_to_search} company offer?"
    )
    return str(response)

@timeit
def generate_ig_post(prompt: str = "") -> str:
    # mustdo: Reformulate history!
    """
    Function to generate a post for Instagram using a predefined prompt and chatgpt
    """
    openai.api_key = settings.OPENAI_API_TOKEN
    
    answer = "Please specify a prompt"
    
    if messages is None:
        messages = [
            {
                "role": "system",
                "content": "Sei un sistema intelligente che genera ed edita dei post per instagram",
            }
        ]
        
    if prompt!="":
        messages.append(
            {"role": "user", "content": prompt},
        )
        chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
        # mustdo, return more than one choice
        reply = chat.choices[0].message.content
        messages.append({"role": "assistant", "content": reply})
        answer = reply

    return answer, messages

@timeit
def generate_img_description(image: BytesIO, model: str = settings.MODEL_BLIP) -> str:
    """
    Function to generate a description of an image using blip2
    """
    client = replicate.Client(api_token=settings.REPLICATE_API_KEY)

    output = client.run(model_version=model, input={"image": image})
    return str(output)
