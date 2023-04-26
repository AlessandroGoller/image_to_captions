""" Home page streamlit """

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.services.langchain import search_info_of_company
from app.utils.streamlit_utils.auth import is_logged_in

session_state = st.session_state.setdefault("auth", {}) # retrieve the session state

if not is_logged_in(session_state):
    switch_page("login")
st.success(f"Logged in as {session_state['username']}.")
st.button("Log out", on_click=lambda: session_state.clear()) # clear the session

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

