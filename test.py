
from app.services.langchain import search_info_of_company

if __name__ == "__main__":
    question = "Which NFL team won the Super Bowl in the 2010 season?"

    a = search_info_of_company(question)
    print(a)


