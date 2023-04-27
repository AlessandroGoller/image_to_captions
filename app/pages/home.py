""" Home page streamlit """

import csv
import os
import time

import instaloader
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.services.langchain import search_info_of_company
from app.utils.ig_scraping import GetInstagramProfile
from app.utils.streamlit_utils.auth import is_logged_in

ARCHIVE_PATH = "archive"

session_state = st.session_state.setdefault("auth", {}) # retrieve the session state

if not is_logged_in(session_state):
    switch_page("login")
st.success(f"Logged in as {session_state['email']}.")
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

# Input per la pagina instagram
instagram_input = st.text_input("Inserisci il link della tua pagina instagram:")
# Scraping pagina instagram
if st.button("Link instagram page"):
    # Check if the page is already in the archive
    if(instagram_input+".csv" in os.listdir(ARCHIVE_PATH)):
        # Load the data
        pass
        # TODO
    else:
        # Scraping
        # TODO decide if to scrape here or throw a message to invite the scraping
        with st.spinner("We are connecting the instagram page..."):
            cls = GetInstagramProfile()
            with open(instagram_input+".csv", "w", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                posts = instaloader.Profile.from_username(cls.L.context, instagram_input).get_posts()
                for post in posts:
                    # Put sleep to avoid too fast requests
                    time.sleep(1)
                    writer.writerow(["post",
                                    str(post.date), post.mediaid,
                                    post.profile, post.caption, post.location,
                                    post.likes, post.comments]
                                )

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

