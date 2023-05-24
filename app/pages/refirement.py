"""
Module streamlit
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

logger = configure_logger()

session_state = st.session_state.setdefault("auth", {})

if not is_logged_in(session=session_state):
    switch_page("login")

if not session_state.get("image_caption", False):
    switch_page("action")  # to change it in home

st.write(session_state.get("image_caption"))
edit_text = st.text_input("Desideri modificare il testo?\nScrivi che tipo di modifica desideri\nEsempi: Fai la descrizione 3 righe più lunga.\n Rendila più amichevole\n...")

prompt = f""" Modifica la seguente descrizione per un post instagram: "{session_state["image_caption"]}" in base a questo input: "{edit_text}" """

if st.button("new test?"):
    del session_state["image_cache"]
    del session_state["image_description"]
    del session_state["image_caption"]
