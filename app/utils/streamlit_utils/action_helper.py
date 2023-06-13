""" Helper for action streamlit """
import streamlit as st
from app.utils.logger import configure_logger

logger = configure_logger()

def  add_info_sponsor(session_state:dict)->str:
    """ Extract from the session state, info regarding the sponsor of a product or event"""
    if "option_product" in session_state:
        logger.info("Sponsor a Product")
        text = f"""The post is use for sponsor this product: {session_state.get("option_product", "")}"""
        logger.info(text)
        return text
    if "option_event" in session_state:
        event_option = session_state["option_event"]
        logger.info("Sponsor an event")
        text = ""
        text += f"""The event will be locate in {event_option[0]}. """\
            if event_option[0] != "" else ""
        text += f"""The event will be in date: {event_option[1]}. """\
            if event_option[1] != "" else ""
        text += f"""There more info about the event: {event_option[2]}. """\
            if event_option[2] != "" else ""
        logger.info(text)
        return text
    return ""

def update_post(option):
    if option == "Post 1":
        st.session_state["post"] = st.session_state["post"][0]
    elif option == "Post 2":
        st.session_state["post"] = st.session_state["post"][1]
    elif option == "Post 3":
        st.session_state["post"] = st.session_state["post"][2]
    st.session_state["messages"].append({"role": "assistant", "content": st.session_state["post"]})
    
def create_new_post():
    if "prompt" in st.session_state:
        del st.session_state["prompt"]
    if "post" in st.session_state:
        del st.session_state["post"]
    if "temp_post" in st.session_state:
        del st.session_state["temp_post"]
    if "messages" in st.session_state:
        del st.session_state["messages"]
    if "temp_messages" in st.session_state:
        del st.session_state["temp_messages"]
    