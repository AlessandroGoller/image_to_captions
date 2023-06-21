""" Streamlit Telegram Page """


import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.crud.user import get_id_user_by_email
from app.services.telegram_bot import get_telegram_url
from app.utils.logger import configure_logger
from app.utils.streamlit_utils.auth import is_logged_in

logger = configure_logger()

if not is_logged_in(session_state=st.session_state):
    switch_page("login")

id_user: str = get_id_user_by_email(email=st.session_state["email"])
telegram_url = get_telegram_url(user_id=id_user)
# use markdown for link
st.write(telegram_url)
