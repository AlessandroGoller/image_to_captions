"""
Module streamlit
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.services.langchain import generate_ig_post
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

# Faster switch to other pages if some criterion are not met
session_state = st.session_state.setdefault("auth", {})
if not is_logged_in(session=session_state):
    switch_page("login")

if not session_state.get("post", False):
    switch_page("action")

logger = configure_logger()

col1, col2 = st.columns(2)

def infinite_edit_post(post:str, modify_request:str)->None:
    """ Function to continue to edit the post """
    if(modify_request == ""):
        st.write("Per favore, inserisci come vuoi modificare il post")
    else:
        prompt = f""" Modifica la seguente descrizione per un post instagram:
                    "{post}" in base a questo input: "{modify_request}" """
        post_edited = generate_ig_post(prompt)
        session_state["temp_post"] = post_edited

st.write("Il post che hai scelto è:")
st.write(f"{session_state['post']}")

st.write("Inserisci un testo che spieghi come vuoi modificare il post! \nEsempi: \n\
        - Voglio che il post sia più ironico\n\
        - Voglio che il post menzioni il nostro prodotto [nomeprodotto]")

modify_request = st.text_input("Come vuoi che venga modificato?", value="")

if st.button("Modifica il post!"):
    infinite_edit_post(post=session_state["post"], modify_request=modify_request)

if "temp_post" in session_state:
    st.write("Post modificato")
    st.write(f"{session_state['temp_post']}")

    # Choose between the old and new post
    option = st.selectbox(
        "Quale post desideri mantenere?",
        ("Originale", "Modificato"),
        label_visibility="visible")

    if st.button("Scegli quale post mantenere"):
        if option == "Modificato":
            session_state["post"] = session_state["temp_post"]
            del session_state["temp_post"]
            st.experimental_rerun()

if st.button("Voglio creare un altro post!"):
    if "image_cache" in session_state:
        del session_state["image_cache"]
    if "image_description" in session_state:
        del session_state["image_description"]
    if "prompt" in session_state:
        del session_state["prompt"]
    if "post" in session_state:
        del session_state["post"]
    if "temp_post" in session_state:
        del session_state["temp_post"]
    # Rerun the script
    st.experimental_rerun()

