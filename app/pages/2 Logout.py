"""
Module streamlit for logout
"""
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.utils.logger import configure_logger

logger = configure_logger()

# Delete all the items in Session state
for key, _ in st.session_state.items():
    del st.session_state[key]

switch_page("login")
