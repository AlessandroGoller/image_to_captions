"""
Module streamlit
"""
from typing import Optional

import streamlit as st
from deep_translator import GoogleTranslator
from stqdm import stqdm
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import get_company_by_user_id
from app.crud.instagram import create_instagram, get_last_n_instagram
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.schema.instagram import InstagramCreate
from app.services.ig_scraping import GetInstagramProfile
from app.services.langchain import (
    generate_ig_post,
    generate_img_description,
)
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

# Maybe to speed up loading?
session_state = st.session_state.setdefault("auth", {})  # retrieve the session state

if not is_logged_in(session=session_state):
    switch_page("login")

LAST_N_POST = 20

logger = configure_logger()
translator = GoogleTranslator(source="en", target="it")

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
            # Generate image description
            description_image: str = generate_img_description(
                session_state["image_cache"]
            )
            # Translate to italian
            description_image = translator.translate(text=description_image)

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
            with st.spinner("Preparation.."):
                client = GetInstagramProfile()
                company = get_company_by_user_id(user_id=user.user_id)
                if company is None:
                    raise ValueError("No company inserted, please insert it")
                instagram_account:str = company.url_instagram
                if instagram_account is None or instagram_account=="":
                    raise ValueError("No instagram account inserted, please insert it")
                data = client.get_post_info_json(instagram_account,last_n_posts=LAST_N_POST)
            
            company_id = company.id_company
            post_inserted = 0
            post_analyzed = 1 # QUEST: Why it starts from 1?
            for single_post in stqdm(data, desc="Scraping Instagram"):
                instagram_post = InstagramCreate(
                        post=single_post.get("post"),
                        id_user=user.user_id,
                        id_company=company_id,
                        image_description=single_post.get("image_description", None),
                        hashtags=single_post.get("hashtags", None).replace(",",";"),
                        mentions=single_post.get("mentions", None).replace(",",";"),
                        tagged_users=single_post.get("tagged_users", None).replace(",",";"),
                        likes=single_post.get("likes", None),
                        comments=single_post.get("comments", None),
                        date=single_post.get("date", None),
                        location=single_post.get("location", None),
                        typename=single_post.get("typename", None),
                        mediacount=single_post.get("mediacount", None),
                        title=single_post.get("title", None),
                        posturl=single_post.get("posturl", None),
                    )
                if create_instagram(instagram = instagram_post):
                    post_inserted+=1
                post_analyzed+=1 # QUEST: What it is used for?
            logger.info(f"Inserted {post_inserted} on account ig: {company.url_instagram}")
            st.success(f"Finish Scraping, {post_inserted} post scraped")
            sample_posts = get_last_n_instagram(
                company_id=company.id_company, number_ig=20
            )

        prompt = "Fornisci il testo da utilizzare nel post di instagram, seguendo il formato degli esempi che fornisco. Gli esempi sono:" # noqa
        for example in sample_posts[:LAST_N_POST]: # type: ignore
            prompt += ' "' + str(example.post) + '",'

        prompt = prompt[:-1] # Remove the comma
        session_state["prompt"] = prompt

        if st.button("Genera il post!") and not session_state.get("post", False):
            with st.spinner("Sto generando il post.."):
            # Add the image description
                prompt = session_state["prompt"]
                prompt += ". Inoltre, personalizza il post in base alla descrizione dell'immagine associata. La descrizione dell'immagine è: " + session_state["image_description"] + ". Inserisci le emoji più opportune. Inserisci gli hashtags più opportuni. Attieniti al tono di voce dell'azienda." # noqa
                # Update the prompt
                session_state["prompt"] = prompt
                # Here I generate the first message specifying the role in this case
                messages = [
                {
                    "role": "system",
                    "content": "Sei un sistema intelligente che genera dei post per instagram",
                }
                ]
                post, messages = generate_ig_post(prompt, messages=messages)
                # Save the messages
                session_state["messages"] = messages
                session_state["post"] = post

    # Mostrare post
    if session_state.get("post", False):
        st.write("Ecco il tuo post")
        st.write(session_state["post"])

        if st.button("Vorrei modificare il post!"):
            switch_page("refinement")

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
