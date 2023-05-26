""" Module utils for streamlit auth """

import bcrypt

from app.crud.user import create_user, get_user_by_email
from app.schema.user import UserCreate


def verify_login(email: str, password: str) -> bool:
    """
    Verifica se l'utente con username e password esiste nella lista degli utenti registrati
    e se le credenziali sono corrette.
    """
    email = email.strip()
    user = get_user_by_email(email=email)
    if user is None:
        return False
    stored_password = user.password
    return bool(
        bcrypt.checkpw(password.encode("utf-8"), stored_password.encode("utf-8"))
    )


def register_user(email: str, password: str) -> bool:
    """
    Registra un nuovo utente con email e password.
    Restituisce True se la registrazione è andata a buon fine,
    False se l'username è già stato utilizzato.
    """
    email = email.strip()
    user = get_user_by_email(email=email)
    if user is not None:
        return False
    data = UserCreate(name="Noname", email=email, password=password)
    user = create_user(user=data)
    if user is None:
        return False
    return True


def is_logged_in(session: dict[str, bool]) -> bool:
    """
    Verifica se l'utente è già loggato o meno.
    """
    return session.get("is_logged_in", False)
