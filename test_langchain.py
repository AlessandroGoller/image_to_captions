#from app.services.langchain import search_info_of_company

#test = search_info_of_company("Salewa")
# Mostrare caption
#print(test)

from loguru import logger

from transformers import AutoTokenizer, AutoModelForCausalLM
logger.info("first imports")

#model_name = "cerebras/Cerebras-GPT-2.7B"
#tokenizer = AutoTokenizer.from_pretrained(model_name)

logger.info("before model")

#model = AutoModelForCausalLM.from_pretrained(model_name)

logger.info("after model")

from transformers import pipeline

logger.info("Pipeline")
#pipe = pipeline(
#    "text-generation", model=model, tokenizer=tokenizer,
#    max_new_tokens=100, early_stopping=True, no_repeat_ngram_size=2
#)

from langchain.llms import HuggingFacePipeline

logger.info("llm")
#llm = HuggingFacePipeline(pipeline=pipe)
from langchain import HuggingFaceHub
from app.dependency import get_settings

settings = get_settings()

llm = HuggingFaceHub(repo_id="google/flan-t5-xl",
                            model_kwargs={"temperature":0, "max_length":512},
                            huggingfacehub_api_token = settings.HUGGINGFACEHUB_API_TOKEN)

from langchain.llms import OpenAI
#llm = OpenAI(model_name="text-davinci-003", openai_api_key=settings.OPENAI_API_TOKEN)

from langchain import SerpAPIWrapper
from langchain.agents import Tool
from langchain.agents import load_tools
from langchain.agents import initialize_agent



logger.info("finish import")


serpapi = SerpAPIWrapper(serpapi_api_key='...')
#tools = [
#    Tool(
#        name = "Search",
#        func=serpapi.run,
#        description="useful for when you need to find a company"
#    )
#]
tools = load_tools(["serpapi"], llm=llm, serpapi_api_key=settings.SERPAPI_API_KEY)

logger.info("after tools")
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

logger.info("after initialize")
#agent.run(input="Brief description of the Salewa Italy company, what is and what they do?")
agent.run("What products or services does Salewa company offer?")

#agent.run(input="Breve descrizione di cosa si occupa e cosa vende l'azienda Salewa?")
logger.info("Finish")
logger.info(agent)
