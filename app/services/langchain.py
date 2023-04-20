""" Module for langchain """

from langchain import HuggingFaceHub, LLMChain, PromptTemplate
from langchain.llms import OpenAI
from loguru import logger

from app.dependency import get_settings

settings = get_settings()


def prepare_llm()->HuggingFaceHub:
    """Return the llm"""
    if "HUGGINGFACEHUB_API_TOKEN" in settings and settings.HUGGINGFACEHUB_API_TOKEN is not None:
        logger.info("Using Hugging_face as llm")
        # initialize Hub LLM
        llm = HuggingFaceHub(
                repo_id="google/flan-t5-xl",
            model_kwargs={"temperature":1e-10},
            huggingfacehub_api_token = settings.HUGGINGFACEHUB_API_TOKEN
        )
    else:
        logger.info("Using OpenAI as llm")
        llm = OpenAI(model_name="text-davinci-003", openai_api_key=settings.OPENAI_API_TOKEN)

    return llm

def search_info_of_company(name_to_search:str)->str:
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

    template = """Name: {name}

    Info: """
    prompt = PromptTemplate(
            template=template,
        input_variables=["name"]
    )
    llm = prepare_llm()
    # create prompt template > LLM chain
    llm_chain = LLMChain(
        prompt=prompt,
        llm=llm
    )

    # ask the user question about NFL 2010
    return str(llm_chain.run(name_to_search))
