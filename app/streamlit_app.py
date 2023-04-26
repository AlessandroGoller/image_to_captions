""" Module for Streamlit """

import streamlit as st

from app.services.langchain import search_info_of_company


# Funzione per generare caption per l'immagine
def generate_caption(name:str, link:str)->str:
    """Generate Info from the data """
    # Inserire il codice per generare le caption qui
    return "Capitolo 1: " + name + " è un'azienda di successo con un sito web professionale" +link

st.set_page_config(page_title="Image to Captions", page_icon=":guardsman:", layout="wide")
st.title("Image to Captions")

# Input per l'azienda
name_input = st.text_input("Inserisci il nome dell'azienda:")

if st.button("Find description"):
    with st.spinner("Wait for it..."):
        test = search_info_of_company(name_input)
        st.success("Done!")
    # Mostrare caption
    st.write(test)

# Input per il sito web
site_input = st.text_input("Inserisci il link del sito web:")

# Aggiungi una sezione per caricare l'immagine
uploaded_file = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])

# Aggiungi il pulsante 'send'
if st.button("Send"):
    # Verifica che sia stata caricata una immagine
    if uploaded_file is not None:
        st.write("immagine caricata")
    else:
        # Mostrare un avviso se l'utente non ha caricato un'immagine
        st.warning("Please upload an image.")


# Generare caption per l'immagine
caption = generate_caption(name_input, site_input)
