"""
Module streamlit
"""

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

logger = configure_logger()

session_state = st.session_state.setdefault("auth", {})

if not is_logged_in(session=session_state):
    switch_page("login")

if not session_state.get("post", False):
    switch_page("home")

st.write(session_state.get("post"))

if st.button("new test?"):
    del session_state["image_cache"]
    del session_state["image_description"]
    del session_state["image_caption"]
