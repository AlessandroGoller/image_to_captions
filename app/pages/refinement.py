"""
Module streamlit
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from app.services.langchain import generate_ig_post

from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

logger = configure_logger()

session_state = st.session_state.setdefault("auth", {})

if not is_logged_in(session=session_state):
    switch_page("login")

if not session_state.get("post", False):
    switch_page("home")

def infinite_edit_post(post:str)->None:
    """ Function to continue to edit the post """
    new_text = st.text_input("Come vuoi che venga modificato?")
    if st.button("Genero il post?"):
        new_prompt = f""" Modifica la seguente descrizione per un post instagram: "{post}" in base a questo input: "{new_text}" """
        post_edited = generate_ig_post(new_prompt)
        session_state["temp_post"] = post_edited
        st.write(post_edited)
        if st.button("Modificare ancora?"):
            infinite_edit_post(post=post_edited)
st.write(session_state.get("post"))

if session_state.get("temp_post", False):
    st.write(f"Nuovo Testo temporaneo:\n{session_state['temp_post']}\n")

edit_text = st.text_input("""Desideri modificare il testo?\nScrivi che tipo di modifica desideri\n
    Esempi: Fai la descrizione 3 righe più lunga.\n Rendila più amichevole\n...""")
if st.button("Rigenerare il post?"):
    prompt = f""" Modifica la seguente descrizione per un post instagram:
        "{session_state["post"]}" in base a questo input: "{edit_text}". """
    new_post = generate_ig_post(prompt)
    session_state["temp_post"] = new_post
    st.write(new_post)
    if st.button("Modificare ancora?"):
        infinite_edit_post(post=new_post)

    if st.button("Salvare?"):
        session_state["post"] = session_state["temp_post"]

if st.button("new test?"):
    del session_state["image_cache"]
    del session_state["post"]
    del session_state["image_description"]
    del session_state["temp_post"] # se non esiste funziona comunque o si rompe?

