""" Module for Streamlit """

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

st.set_page_config(
    page_title="Awesome IG posts", page_icon=":guardsman:", layout="wide"
)
st.title("Awesome Instagram posts")


def main() -> None:
    """Main streamlit"""
    switch_page("login")


if __name__ == "__main__":
    main()
