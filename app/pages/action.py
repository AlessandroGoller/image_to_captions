"""
Module streamlit
"""
from typing import Optional

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import get_company_by_user_id
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.services.ig_scraping import load_post_captions_from_json
from app.services.langchain import (
    generate_ig_post,
    generate_img_description,
)
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

ARCHIVE_PATH = "archive"

logger = configure_logger()

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
    instagram_input = str(company.url_instagram)
    prompt = "Fornisci il testo da utilizzare nel post di instagram, \
            seguendo il formato degli esempi che fornisco. Gli esempi sono:"

    uploaded_file = st.file_uploader("Carica un'immagine", type=["png", "jpg", "jpeg"])
    # Aggiungi il pulsante 'send'
    if st.button("Send"):
        # Verifica che sia stata caricata una immagine
        if uploaded_file is not None:
            # Generation with openai api
            if st.button("Generate description"):
                all_captions = load_post_captions_from_json(
                    ARCHIVE_PATH + "/" + instagram_input + ".json"
                )
                for example in all_captions[:20]:
                    prompt += '"' + example + '",'
                prompt = prompt[:-1]

                with st.spinner("Wait for it..."):
                    # TODO: add in the prompt the info of the company
                    # Use blip 2 for image description
                    description_image: str = generate_img_description(uploaded_file)
                    description_image = st.text_input(
                        "Descrizione dell'immagine da utilizzare:", description_image
                    )

                if st.button("Generate description for the post?"):
                    # Add the image description
                    prompt += (
                        ". Inoltre, personalizza il post in base alla descrizione dell'immagine associata. La\
                        descrizione dell'immagine è: "
                        + description_image
                        + ". Inserisci le emoji più opportune. Inserisci gli hasthatgs più opportuni.\
                        Attieniti al tono di voce dell'azienda."
                    )

                    post = generate_ig_post(prompt)
                    st.success("Done!")
                    # Mostrare post
                    st.write(post)
        else:
            # Mostrare un avviso se l'utente non ha caricato un'immagine
            st.warning("Please upload an image.")


