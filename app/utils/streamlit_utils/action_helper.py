""" Helper for action streamlit """

from app.utils.logger import configure_logger

logger = configure_logger()

def add_info_sponsor(session_state:dict)->str:
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
        text += f"""The event will be locate in {event_option[0]}"""\
            if event_option[0] != "" else ""
        text += f"""The event will be in date: {event_option[1]}"""\
            if event_option[1] != "" else ""
        text += f"""There more info about the event: {event_option[2]}"""\
            if event_option[2] != "" else ""
        logger.info(text)
        return text
    return ""
