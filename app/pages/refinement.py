"""
Streamlit page for the refinement step of the post.
Refinement should start after the first generation of the post, and must
continue until the user is satisfied with the result.
The user can choose to modify the post as many times as he wants.
Added a simple switch that let the user choose between the old post and the modified one.
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.services.langchain import modify_ig_post
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

# Faster switch to other pages if some criterion are not met
session_state = st.session_state.setdefault("auth", {})

if not is_logged_in(session=session_state):
    switch_page("login")

if not session_state.get("post", False):
    switch_page("action")

logger = configure_logger()

# UTILS FUNCTIONS ############################################################################

def infinite_edit_post(modify_request:str)->None:
    """ Function to continue to edit the post """
    if(modify_request == ""):
        st.write("Per favore, inserisci come vuoi modificare il post")
    else:
        # Create the messages for the modify_ig_post function
        messages = [
                {
                    "role": "system",
                    "content": "Sei un sistema intelligente che ha generato un post per instagram ed ora deve modificarlo seguendo le richieste dell'utente", # noqa
                }
        ]
        messages.append(session_state["messages"][-1]) # The last message is the reply by the LM with the original post
        prompt = f""" Modifica il post che hai creato precedentemente in base alla mia richiesta: \"{modify_request}\". Non aggiungere ulteriori premesse, genera solo il post modificato.""" # noqa
        post_edited, temp_messages = modify_ig_post(prompt, messages=messages)
        session_state["temp_post"] = post_edited
        session_state["temp_messages"] = temp_messages

def clear_mod_request() -> None:
    """ Function to clear the modification request """
    st.session_state["mod_request"] = ""
###############################################################################################

st.write("**Il post che hai scelto è:**") # Waiting for the possibility to pick a post from a list
st.write(f"{session_state['post']}")

st.write("""**Inserisci un testo che spieghi come vuoi modificare il post! Esempi:**
         - Voglio che il post sia più ironico
         - Voglio che il post menzioni il nostro prodotto [nomeprodotto]""")

modify_request = st.text_input("Come vuoi che venga modificato?", key="mod_request")

if st.button("Modifica il post!"):
    with st.spinner("Sto modificando il post.."):
        infinite_edit_post(modify_request=modify_request)

if "temp_post" in session_state:
    st.write("Post modificato")
    st.write(f"{session_state['temp_post']}")

    # Choose between the old and new post
    option = st.selectbox(
        "Quale post desideri mantenere?",
        ("Originale", "Modificato"),
        label_visibility="visible")

    if st.button("Scegli quale post mantenere", on_click=clear_mod_request):
        if option == "Modificato":
            session_state["post"] = session_state["temp_post"]
            session_state["messages"] = session_state["temp_messages"]
            del session_state["temp_post"]
            del session_state["temp_messages"]
        else:
            del session_state["temp_post"]
            del session_state["temp_messages"]

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
    if "messages" in session_state:
        del session_state["messages"]
    if "temp_messages" in session_state:
        del session_state["temp_messages"]
    # Rerun the script
    st.experimental_rerun()

