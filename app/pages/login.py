"""
Module streamlit for loggin
"""
import streamlit as st
from streamlit_extras.switch_page_button import switch_page

from app.utils.streamlit_utils.auth import is_logged_in, register_user, verify_login


def show_login_page()->None:
    """ show_login_page """
    st.header("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    login_button = st.button("Log in")
    if login_button:
        if verify_login(username, password):
            st.success("Logged in successfully.")
            session_state["is_logged_in"] = True
            session_state["username"] = username
            st.experimental_rerun() # reload the page
        else:
            st.error("Invalid username or password.")

def show_register_page()->None:
    """ show_register_page """
    st.header("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")
    register_button = st.button("Register")
    if register_button:
        if password != confirm_password:
            st.error("Passwords do not match.")
        elif register_user(username, password):
            st.success("Registered successfully.")
            session_state["is_logged_in"] = True
            session_state["username"] = username
            st.experimental_rerun() # reload the page
        else:
            st.error("Username already taken.")

def show_auth_page()->None:
    """ show_auth_page """
    if is_logged_in(session_state):
        switch_page("home")
    else:
        st.warning("Not logged in.")
        st.write("")
        mode = st.radio("Choose your mode", ("Login", "Register"))
        if mode == "Login":
            show_login_page()
        else:
            show_register_page()


session_state = st.session_state.setdefault("auth", {}) # retrieve the session state
show_auth_page()
