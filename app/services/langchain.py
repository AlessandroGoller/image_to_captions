""" Module for langchain """

from langchain import HuggingFaceHub  #, LLMChain, PromptTemplate
from langchain.agents import initialize_agent, load_tools
from langchain.llms import OpenAI
from loguru import logger

from app.dependency import get_settings

settings = get_settings()


def prepare_llm()->HuggingFaceHub:
    """Return the llm"""
    if settings.HUGGINGFACEHUB_API_TOKEN is not None:
        logger.info("Using Hugging_face as llm")
        # initialize Hub LLM
        llm = HuggingFaceHub(repo_id="google/flan-t5-xl",
                            model_kwargs={"temperature":0, "max_length":512},
                            huggingfacehub_api_token = settings.HUGGINGFACEHUB_API_TOKEN)
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
    llm = prepare_llm()
    tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=settings.SERPAPI_API_KEY)
    agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)
    response = agent.run(f"What products or services does {name_to_search} company offer?")
    return response

    '''
    OLD
    template = """Company name : {name}

    Brief explanation of what the company consists of and what it does: """
    prompt = PromptTemplate(
            template=template,
        input_variables=["name"]
    )
    llm = prepare_llm()
    # create prompt template > LLM chain
    llm_chain = LLMChain(
        prompt=prompt,
        verbose=True,
        llm=llm
    )
    # ask the user question about NFL 2010
    return str(llm_chain.run(name_to_search))
    '''
