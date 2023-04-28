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
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

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

st.write("Page in progress")
