"""
Module streamlit for profile settings
"""
from typing import Optional

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import create_company, get_company_by_user_id, remove_account_ig, update_company
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.schema.company import CompanyCreate, CompanyInfoBase
from app.services.langchain import search_info_of_company
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in
from app.utils.streamlit_utils.profile_helper import get_profile_pic

logger = configure_logger()


def company_exist(company: Company) -> None:
    """Case in which the company already exist"""
    # Update session state for button behavior
    if "description" not in st.session_state:
        st.session_state["description"] = company.description
    language = st.text_input("In what language the prompt has to be?\n\
                             If Auto, the AI will decide", str(company.language))
    company_name = st.text_input("Company Name:", str(company.name))
    description = st.text_input(
        "Company description:",
        str(company.description) if company.description is not None else "",
    )
    if "description" not in st.session_state:
        if st.button("Find company description?"):
            with st.spinner("Wait for it..."):
                description = search_info_of_company(company_name)
                st.session_state["description"] = description
                st.success("Done!")
            # Mostrare caption
            _ = st.text_input("Description, AI generated", description)
    website = st.text_input(
        "Company Website:", str(company.website) if company.website is not None else ""
    )
    if company.url_instagram is not None and company.url_instagram != "":
        instagram_url = str(company.url_instagram)
        st.write("Instagram Account: " + str(company.url_instagram))
        if st.button("Delete Instagram Account. N.B. Cambiare account necessiterà un po di tempo alla prima creazione della caption"):  # noqa
            remove_account_ig(id_company=company.id_company)
            st.experimental_rerun()  # reload the page
    else:
        instagram_url = st.text_input(
            "Instagram Name:",
            str(company.url_instagram) if company.url_instagram is not None else "",
        )

    # Print the profile pic
    if company.url_instagram is not None and company.url_instagram!="":
        profile_pic_url = get_profile_pic(company)
        if profile_pic_url is not None:
            st.image(profile_pic_url, caption="Immagine Instagram")

    if st.button("Save Info"):
        company_created = CompanyInfoBase(
            name=company_name if company_name is not None else "",
            description=st.session_state["description"],
            website=website,
            language=language,
            url_instagram=instagram_url,
        )
        if update_company(company=company, company_edit=company_created) is None:
            raise Exception("Error during creation of a Company")
        st.write("Success Save")
        switch_page("action")


def company_not_exist(user: User) -> None:
    """Case in which the company NOT exist"""
    language = st.text_input("In what language the prompt has to be?\nIf Auto, the AI will decide", "Auto")
    company_name = st.text_input("Insert Company Name:","")
    website = st.text_input("Insert Company website:", "")
    instagram_url = st.text_input("Insert Instagram Name:", "")
    description = ""
    if company_name is None or company_name == "":
        st.write("Please Insert the Company Name")
    else:
        if st.button("Find description"):
            with st.spinner("Wait for it..."):
                description = search_info_of_company(company_name)
                st.success("Done!")
            # Mostrare caption
            description = st.text_input("Description, AI generated", description)
    if st.button("Save Info"):
        company_created = CompanyCreate(
            name=company_name,
            description=description,
            website=website,
            url_instagram=instagram_url,
            language=language,
            id_user=user.user_id,
        )
        if create_company(company=company_created) is None:
            raise Exception("Error during creation of a Company")
        else:
            st.write("Success Save")
            switch_page("action")


if not is_logged_in(session_state=st.session_state):
    switch_page("login")

user: Optional[User] = get_user_by_email(email=st.session_state["email"])
if user is None:
    logger.error("Profile Page without having an account")
    raise ValueError("Illegal position")
company: Optional[Company] = get_company_by_user_id(user_id=user.user_id)

if company is None:
    company_not_exist(user=user)
else:
    logger.info(f"{user.email=} -> {company.name}")
    company_exist(company=company)
