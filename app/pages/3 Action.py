"""
Module streamlit
"""
from typing import Optional

import streamlit as st
from deep_translator import GoogleTranslator
from numpy import array
from PIL import Image
from stqdm import stqdm
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import get_company_by_user_id
from app.crud.instagram import create_instagram, get_last_n_instagram
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.schema.instagram import InstagramCreate
from app.schema.post_creation import PostCreationCreate
from app.services.ig_scraping import GetInstagramProfile
from app.services.langchain import (
    generate_ig_post,
    generate_img_description,
)
from app.utils.logger import configure_logger
from app.utils.openai import tokenization
from app.utils.streamlit_utils.action_helper import add_info_sponsor, create_new_post, update_post
from app.utils.streamlit_utils.auth import is_logged_in

if not is_logged_in(session_state=st.session_state):
    switch_page("login")

LAST_N_POST = 20

logger = configure_logger()
translator = GoogleTranslator(source="en", target="it")

user: Optional[User] = get_user_by_email(email=st.session_state["email"])
if user is None:
    logger.error("Profile Page without having an account")
    raise ValueError("Impossible Position")
company: Optional[Company] = get_company_by_user_id(user_id=user.user_id)

if company is None:
    switch_page("profile")
else:
    uploaded_file = st.file_uploader(
        "Carica un'immagine", type=["png", "jpg", "jpeg"]
    )
    if uploaded_file:
        # Se non era ancora presente il file
        if "image_cache" not in st.session_state:
            st.session_state["image_cache"] = uploaded_file
        # Se il file è diverso da quello che avevo
        elif uploaded_file != st.session_state["image_cache"]:
            st.session_state["image_cache"] = uploaded_file
            # Remove old variables
            if "image_description" in st.session_state:
                del st.session_state["image_description"]
            if "prompt" in st.session_state:
                del st.session_state["prompt"]
            if "post" in st.session_state:
                del st.session_state["post"]

    if st.session_state.get("image_cache", False):
        st.image(st.session_state["image_cache"], caption="La tua immagine")

    # If I have the image, but not the description, I can go on generating the description
    if not st.session_state.get(
        "image_description", False
    ) and st.session_state.get("image_cache", False):
        # Get the image description
        with st.spinner("Sto cercando una descrizione per l'immagine.."):
            # Generate image description
            description_image: str = generate_img_description(
                st.session_state["image_cache"]
            )
            # Translate to italian
            description_image = translator.translate(text=description_image)

            # Store it
            st.session_state["image_description"] = description_image

    if st.session_state.get(
        "image_description", False
    ):
        description_image = st.text_input(
                "Modifica la descrizione se non ti soddisfa:",
                st.session_state["image_description"],
                key="description_image"
            )

        # Store it
        st.session_state["image_description"] = description_image

        # Option list
        options = [None, "Product", "Event"]
        index_option = st.session_state.get("index_options_sponsor", 0)
        selected_option = st.selectbox("Do you want to sponsor something? Choose an option:",
                                    options, index=index_option)
        st.session_state["index_options_sponsor"] = options.index(selected_option)
        if selected_option == "Product":
            description = st.text_input("Enter a brief description:",st.session_state.get("option_product", ""))
            st.session_state["option_product"] = description
            st.session_state.pop("option_event", None)
        elif selected_option == "Event":
            if "option_event" in st.session_state:
                location = st.text_input("Enter the event location:",st.session_state.get("option_event")[0])
                date = st.date_input("Enter the event date:",st.session_state.get("option_event")[1])
                additional_info = st.text_area("Enter additional information:",st.session_state.get("option_event")[2])
            else:
                location = st.text_input("Enter the event location:")
                date = st.date_input("Enter the event date:")
                additional_info = st.text_area("Enter additional information:")
            st.session_state["option_event"] = [location,date,additional_info]
            st.session_state.pop("option_product", None)
        else:
            st.session_state.pop("option_product", None)
            st.session_state.pop("option_event", None)

        if st.button("Genera il post!") and\
            not st.session_state.get("post", False) and\
            st.session_state.get("image_description", False):

            # Generate the prompt for the post
            sample_posts = get_last_n_instagram(
                company_id=company.id_company, number_ig=20
            )
            if sample_posts is None or len(sample_posts)<1:
                with st.spinner("Preparation, please wait"):
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
                logger.info(f"Inserted {post_inserted=} on account ig: {company.url_instagram}")
                st.success(f"Finish Scraping, {post_inserted} post scraped")
                sample_posts = get_last_n_instagram(
                    company_id=company.id_company, number_ig=20
                )

            with st.spinner("Sto generando tre post da cui potrai scegliere.."):
                # Create the prompt
                prompt = "Genera un post per instagram, seguendo il formato degli esempi che fornisco:" # noqa
                # To be sure, we will add each post until we reach 3500 tokens maximum
                tok = 0
                posts = 0
                if sample_posts is not None:
                    for example in sample_posts:
                        # We insert posts until we reach 3500 tokens
                        # QUEST: are the post in order from the most recent?
                        if (tok+tokenization.num_tokens_from_string(example.post)<3500):
                            prompt += ' "' + str(example.post) + '",'
                            tok += tokenization.num_tokens_from_string(example.post)
                            posts += 1
                        else:
                            break
                else:
                    raise ValueError("No posts found")

                logger.info(f"Inserted {posts} post, corresponding to {tok} tokens, in the prompt")

                prompt = prompt[:-1] # Remove the comma

                prompt += ". Personalizza il post perchè sia adatto ad un'immagine di " + st.session_state["image_description"] + ". Inserisci emoticons e hashtags nel post. Attieniti al formato degli esempi." # noqa
                # Update the prompt
                prompt += add_info_sponsor(session_state=st.session_state)

                # Save the prompt
                st.session_state["prompt"] = prompt

                # Here I generate the first message specifying the role in this case
                messages = [
                {
                    "role": "system",
                    "content": "Sei un sistema intelligente che genera dei post per instagram",
                }
                ]
                posts = generate_ig_post(prompt, messages=messages)
                post_created: PostCreationCreate = PostCreationCreate(
                    user_id = user.user_id,
                    description = st.session_state["image_description"],
                    prompt = "", # prompt -> It will save all the 20 description of IG,
                    posts_created = posts,
                    image_uploaded = array(Image.open(st.session_state["image_cache"])).tobytes()
                )
                # Save the messages
                st.session_state["messages"] = messages
                st.session_state["post"] = posts
                # create_post_creation(post_created) -> There is a problem with ssl connection

    # Mostrare i diversi post generati
    if st.session_state.get("post", False) and type(st.session_state["post"])==list:
        st.write("Post 1:")
        st.write(st.session_state["post"][0])
        st.write("Post 2:")
        st.write(st.session_state["post"][1])
        st.write("Post 3:")
        st.write(st.session_state["post"][2])

        # Choose between the old and new post
        option = st.selectbox(
            "Quale post desideri mantenere?",
            ("Post 1", "Post 2", "Post 3"),
            label_visibility="visible")

        st.button("Scegli quale post mantenere", on_click=update_post, args=(option,))

    # Mostrare il post scelto
    if st.session_state.get("post", False) and type(st.session_state["post"])==str:
        st.write("Il post che hai scelto è:")
        st.write(st.session_state["post"])

        # Render the two buttons to modify or create a new post
        if st.button("Vorrei modificare il post!"):
            switch_page("refinement")

        st.button("Voglio creare un altro post!", on_click=create_new_post)
