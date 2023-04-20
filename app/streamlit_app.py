""" Module for Streamlit """

import streamlit as st


# Funzione per generare caption per l'immagine
def generate_caption(name:str, link:str)->str:
    """Generate Info from the data """
    # Inserire il codice per generare le caption qui
    return "Capitolo 1: " + name + " è un'azienda di successo con un sito web professionale" +link

st.set_page_config(page_title="Image to Captions", page_icon=":guardsman:", layout="wide")
st.title("Image to Captions")

# Input per l'azienda
name_input = st.text_input("Inserisci il nome dell'azienda:")

# Input per il sito web
site_input = st.text_input("Inserisci il link del sito web:")

# Generare caption per l'immagine
caption = generate_caption(name_input, site_input)

# Mostrare caption
st.write(caption)
