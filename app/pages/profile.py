"""
Module streamlit for profile settings
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.company import create_company, get_company_by_user_id, update_company
from app.crud.user import get_user_by_email
from app.model.company import Company
from app.schema.company import CompanyCreate, CompanyInfoBase
from app.services.langchain import search_info_of_company
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

logger = configure_logger()

session_state = st.session_state.setdefault("auth", {}) # retrieve the session state

def company_exist(company:Company)->None:
    """ Case in which the company already exist """
    company_name = st.text_input("Company Name:",str(company.name))
    description = st.text_input("Company description:",str(company.description) if company.description is not None else "")
    website = st.text_input("Company Website:",str(company.website) if company.website is not None else "")
    if st.button("Find NEW description?"):
        with st.spinner("Wait for it..."):
            description = search_info_of_company(company_name)
            st.success("Done!")
        # Mostrare caption
        description = st.text_input("Description, AI generated",description)
    if st.button("Save Info") and company_name is not None and company_name != "":
        company_created = CompanyInfoBase(name=company_name,description=description,website=website)
        if update_company(company=company, company_edit=company_created) is None:
            raise Exception ("Error during creation of a Company")
        else:
            st.write("Success Save")
            switch_page("home")

def company_not_exist()->None:
    """ Case in which the company NOT exist """
    company_name = st.text_input("Insert Company Name:")
    website = st.text_input("Insert Company website:","")
    description = ""
    if company_name is None or company_name=="":
        st.write("Please Insert the Company Name")
    else:
        if st.button("Find description"):
            with st.spinner("Wait for it..."):
                description = search_info_of_company(company_name)
                st.success("Done!")
            # Mostrare caption
            description = st.text_input("Description, AI generated",description)
        if st.button("Save Info"):
            company_created = CompanyCreate(name=company_name,description=description,website=website,id_user=user.user_id)
            if create_company(company=company_created) is None:
                raise Exception ("Error during creation of a Company")
            else:
                st.write("Success Save")
                switch_page("home")

if not is_logged_in(session=session_state):
    switch_page("login")

user = get_user_by_email(email=session_state["email"])
if user is None:
    logger.error("Profile Page without having an account")
    raise Exception ("Illegal position")
company = get_company_by_user_id(user_id=user.user_id)

if company is None:
    company_not_exist()
else:
    logger.info(f"{user.email=} -> {company.name}")
    company_exist(company=company)
