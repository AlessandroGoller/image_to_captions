"""
Module streamlit
"""
from typing import Optional

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import get_company_by_user_id
from app.crud.instagram import get_last_n_instagram
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.services.langchain import (
    generate_ig_post,
    generate_img_description,
)
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in
from googletrans import Translator

ARCHIVE_PATH = "archive"

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
    if not session_state.get("image_cache", False):
        uploaded_file = st.file_uploader(
            "Carica un'immagine", type=["png", "jpg", "jpeg"]
        )
        session_state["image_cache"] = uploaded_file
    if session_state.get("image_cache", False) and not session_state.get(
        "image_description", False
    ):
        if st.button("Generate Description?"):
            prompt = "Fornisci il testo da utilizzare nel post di instagram, \
                    seguendo il formato degli esempi che fornisco. Gli esempi sono:"
            all_captions = get_last_n_instagram(
                company_id=company.id_company, number_ig=20
            )
            if all_captions is None:
                raise ValueError("all_captions is None")
            for example in all_captions[:20]:
                prompt += '"' + str(example) + '",'
            prompt = prompt[:-1]
            with st.spinner("Wait for it..."):
                # TODO: add in the prompt the info of the company
                # Use blip 2 for image description
                description_image: str = generate_img_description(
                    session_state["image_cache"]
                )
                description_image = st.text_input(
                    "Descrizione dell'immagine da utilizzare:", description_image
                )
                session_state["image_description"] = description_image
                session_state["prompt"] = prompt
    if (
        session_state.get("image_cache", False)
        and session_state.get("image_description", False)
        and not session_state.get("image_caption", False)
    ):
        if st.button("Generate Prompt?"):
            # Add the image description
            prompt = session_state["prompt"]
            prompt += (
                ". Inoltre, personalizza il post in base alla descrizione dell'immagine associata. La\
                descrizione dell'immagine è: "
                + session_state["image_description"]
                + ". Inserisci le emoji più opportune. Inserisci gli hasthatgs più opportuni.\
                Attieniti al tono di voce dell'azienda."
            )
            post = generate_ig_post(prompt)
            st.success("Done!")
            session_state["image_caption"] = post
            # Mostrare post
            st.write(post)
    if (
        session_state.get("image_cache", False)
        and session_state.get("image_description", False)
        and session_state.get("image_caption", False)
    ):
        switch_page("refirement")
