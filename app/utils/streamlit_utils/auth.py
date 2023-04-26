""" Module utils for streamlit auth """

import base64
import hashlib

USERS = {
    "admin":"admin"
}

def verify_login(username: str, password: str) -> bool:
    """
    Verifica se l'utente con username e password esiste nella lista degli utenti registrati
    e se le credenziali sono corrette.
    """
    stored_password = USERS.get(username)
    if stored_password is None:
        return False
    return password==stored_password

def register_user(username: str, password: str) -> bool:
    """
    Registra un nuovo utente con username e password.
    Restituisce True se la registrazione è andata a buon fine,
    False se l'username è già stato utilizzato.
    """
    if username in USERS:
        return False
    hashed_password = base64.b64encode(hashlib.sha256(
        password.encode("utf-8")).digest()).decode("utf-8")
    USERS[username] = hashed_password
    return True

def is_logged_in(session:dict[str,bool]) -> bool:
    """
    Verifica se l'utente è già loggato o meno.
    """
    return session.get("is_logged_in", False)
