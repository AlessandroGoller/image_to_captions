
# from app.services.langchain import search_info_of_company

# if __name__ == "__main__":
#     question = "Which NFL team won the Super Bowl in the 2010 season?"

#     a = search_info_of_company(question)
#     print(a)

import replicate
import os
import streamlit as st
from instascrape import *
import pickle
from app.dependency import get_settings

settings = get_settings()


# TODO LOGIN? 
st.set_page_config(page_title="Get your perfect instagram post!", page_icon=":guardsman:", layout="wide")
st.title("Automatic instagram post generator!")

################ PARTE DI INPUT DEI DATI DELL'AZIENDA #################
# Input per l'azienda
name_input = st.text_input("Inserisci il nome dell'azienda:")

# Input per il sito web
site_input = st.text_input("Inserisci il link del sito web:")

instagram_page = st.text_input("Inserisci il link della pagina instagram:")

st.button("Form se non ho le informazioni precedenti")
############### PARTE DI SCRAPING DI INFO DAL SITO/DAL NOME ############
########################################################################
############### COLLEGAMENTO API INSTAGRAM #############################
insta_profile = Profile('https://www.instagram.com/dolomistici/')
insta_profile.scrape()

print(insta_profile.followers)

with open("profile_dump.pkl", "wb") as f:
    pickle.dump(insta_profile, f)
########################################################################
# Mostrare caption
# st.write(caption)

# os.environ["REPLICATE_API_TOKEN"] = "1a7a7943b947b3db05f51b2beb74a87d5d5cd78c"


# image = Image.open("test_img.jpg")

# output = replicate.run(
#     "andreasjansson/blip-2:4b32258c42e9efd4288bb9910bc532a69727f9acd26aa08e175713a0a857a608",
#     input={"image": open("test_img.jpg", "rb")},caption=True,
# )
# print(output)