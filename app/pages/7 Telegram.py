""" Streamlit Telegram Page """


import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.user import get_hash_from_email
from app.dependency import get_settings
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

settings = get_settings()
logger = configure_logger()

if not is_logged_in(session_state=st.session_state):
    switch_page("login")

hash_code: str = get_hash_from_email(email=st.session_state["email"])
telegram_url = f"https://telegram.me/{settings.TELEGRAM_BOT}?start={hash_code}"
# use markdown for link
st.write(telegram_url)
