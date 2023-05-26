"""
Module streamlit
"""
from typing import Optional

import streamlit as st
from googletrans import Translator
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import get_company_by_user_id
from app.crud.instagram import get_last_n_instagram, insert_data_to_db
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.services.ig_scraping import GetInstagramProfile
from app.services.langchain import (
    generate_ig_post,
    generate_img_description,
)
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

LAST_N_POST = 20

logger = configure_logger()
translator = Translator()

session_state = st.session_state.setdefault("auth", {})  # retrieve the session state

if not is_logged_in(session=session_state):
    switch_page("login")

user: Optional[User] = get_user_by_email(email=session_state["email"])
if user is None:
    logger.error("Profile Page without having an account")
    raise Exception("Illegal position")
company: Optional[Company] = get_company_by_user_id(user_id=user.user_id)

if company is None:
    switch_page("profile")
else:
    uploaded_file = st.file_uploader(
        "Carica un'immagine", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        # Se non era ancora presente il file
        if "image_cache" not in session_state:
            session_state["image_cache"] = uploaded_file
        # Se il file è diverso da quello che avevo
        elif uploaded_file != session_state["image_cache"]:
            session_state["image_cache"] = uploaded_file
            # Remove old variables
            if "image_description" in session_state:
                del session_state["image_description"]
            if "prompt" in session_state:
                del session_state["prompt"]
            if "post" in session_state:
                del session_state["post"]


    # If I have the image, but not the description, I can go on generating the description
    if not session_state.get(
        "image_description", False
    ) and session_state.get("image_cache", False):
        # Get the image description
        with st.spinner("Sto cercando una descrizione per l'immagine.."):
            # TODO: add in the prompt the info of the company

            # Generate image description
            description_image: str = generate_img_description(
                session_state["image_cache"]
            )
            # Translate to italian
            description_image = translator.translate(description_image, src="en", dest="it").text

            # Store it
            session_state["image_description"] = description_image

    if "image_description" in session_state:

        description_image = st.text_input(
                "Modifica la descrizione se non ti soddisfa:",
                session_state["image_description"],
                key="description_image"
            )

        # Store it
        session_state["image_description"] = description_image


    # If I have the description, I can go on generating the promtp
    if session_state.get("image_description", False):
        # Generate the prompt for the post
        sample_posts = get_last_n_instagram(
            company_id=company.id_company, number_ig=20
        )
        if sample_posts is None or len(sample_posts)<1:
            with st.spinner("Scraping Instagram Post"):
                client = GetInstagramProfile()
                company = get_company_by_user_id(user_id=user.user_id)
                if company is None:
                    raise ValueError("No company found, try to insert it")
                instagram_account:str = company.url_instagram
                if instagram_account is None or instagram_account=="":
                    raise ValueError("No instagram account inserted, please insert it")
                data = client.get_post_info_json(instagram_account,last_n_posts=LAST_N_POST)
                company_id = company.id_company
                if not insert_data_to_db(data=data,user_id=user.user_id,company_id=company_id):
                    raise ValueError("all_captions is None")
                sample_posts = get_last_n_instagram(
                    company_id=company.id_company, number_ig=20
                )

        prompt = "Fornisci il testo da utilizzare nel post di instagram, \
            seguendo il formato degli esempi che fornisco. Gli esempi sono:"
        for example in sample_posts[:LAST_N_POST]: # type: ignore
            prompt += '"' + str(example.post) + '",'

        prompt = prompt[:-1] # Remove the comma
        session_state["prompt"] = prompt

        if st.button("Genera il post!") and not session_state.get("post", False):
            with st.spinner("Sto generando il post.."):
            # Add the image description
                prompt = session_state["prompt"]
                prompt += (
                    ". Inoltre, personalizza il post in base alla descrizione dell'immagine associata. La\
                    descrizione dell'immagine è: "
                    + session_state["image_description"]
                    + ". Inserisci le emoji più opportune. Inserisci gli hashtags più opportuni.\
                    Attieniti al tono di voce dell'azienda."
                )
                post = generate_ig_post(prompt)
                session_state["post"] = post

    # Mostrare post
    if session_state.get("post", False):
        st.text_area(label = "Post", value=session_state["post"], height=300)

        if st.button("Raffina il tuo post!"):
            switch_page("refinement")
