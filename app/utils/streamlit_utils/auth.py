""" Module utils for streamlit auth """

def is_logged_in(session_state: dict[str, bool]) -> bool:
    """
    Verifica se l'utente è già loggato o meno.
    """
    return session_state.get("is_logged_in", False)
