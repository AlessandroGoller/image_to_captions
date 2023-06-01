"""
Module streamlit for profile settings
"""
import traceback
from typing import Optional

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import create_company, get_company_by_user_id, update_company
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.model.user import User
from app.schema.company import CompanyCreate, CompanyInfoBase
from app.services.ig_scraping import GetInstagramProfile
from app.services.langchain import search_info_of_company
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

logger = configure_logger()

session_state = st.session_state.setdefault("auth", {})  # retrieve the session state


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
    instagram_url = st.text_input(
        "Instagram Name:",
        str(company.url_instagram) if company.url_instagram is not None else "",
    )
    if instagram_url is not None and instagram_url != "":
        try:
            client = GetInstagramProfile()
            path_pic = client.get_profile_pic(instagram_url)
            st.image(path_pic, caption="Immagine Instagram")
        except Exception as error:
            traceback_msg = traceback.format_exc()
            logger.warning(f"Impossible showing the profile pic\n{error}\n{traceback_msg}")
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
        else:
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


if not is_logged_in(session=session_state):
    switch_page("login")

user: Optional[User] = get_user_by_email(email=session_state["email"])
if user is None:
    logger.error("Profile Page without having an account")
    raise Exception("Illegal position")
company: Optional[Company] = get_company_by_user_id(user_id=user.user_id)

if company is None:
    company_not_exist(user=user)
else:
    logger.info(f"{user.email=} -> {company.name}")
    company_exist(company=company)
