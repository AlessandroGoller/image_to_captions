""" Contact form """

import streamlit as st
from validate_email import validate_email

st.title("Contact Form")
st.write("Inserisci le tue informazioni di contatto:")

name = st.text_input("Nome")
email = st.text_input("Email")
message = st.text_area("Messaggio")
submitted = st.button("Invia")

if submitted:
    if name is None or name == "":
        st.write("Please insert the name")
    elif email is None or not validate_email(email):
        # We can add that we use the login email
        st.write("Please insert a correct email")
    else:
        # Esegui le azioni desiderate quando il modulo viene inviato
        # Ad esempio, puoi inviare un'email con i dati del modulo
        st.write("Grazie per averci contattato!")
