""" Module for Streamlit """
# pylint: disable=C0301
# flake8: noqa

import streamlit as st
from streamlit_extras.switch_page_button import switch_page

# Imposta il titolo della pagina e l'icona
st.set_page_config(
    page_title="Automazione Didascalie",
    page_icon="📷"
)

# Titolo principale
st.title("Benvenuti in Automazione Didascalie!")

# Descrizione dell'app
st.markdown(
    """
    Automazione Didascalie è una piattaforma intelligente che utilizza l'intelligenza artificiale per automatizzare la creazione di didascalie per le foto da pubblicare sui social media, con un focus particolare su Instagram.

    Con la nostra tecnologia avanzata, rendiamo il processo di creazione di didascalie veloce, semplice ed estremamente preciso. Non dovrai più preoccuparti di scrivere manualmente le didascalie per ogni foto. La nostra AI si occuperà di tutto!

    ### Come funziona?
    1. Carica la tua foto nel nostro sistema.
    2. La nostra AI analizzerà l'immagine e genererà una didascalia intelligente.
    3. Personalizza la didascalia se desideri apportare modifiche o aggiungi il tuo tocco creativo.
    4. Copia la didascalia e usala per la tua

    Pubblica la tua foto su Instagram insieme alla didascalia perfetta!

    ### Vantaggi dell'Automazione Didascalie:
    Risparmia tempo prezioso: Non perdere più ore a pensare a didascalie creative. Lascia che la nostra AI si occupi di tutto per te.
    Massima precisione: La nostra tecnologia utilizza algoritmi avanzati per generare didascalie altamente rilevanti e coinvolgenti per le tue foto.
    Personalizzazione: Se desideri apportare modifiche o aggiungere il tuo tocco personale, puoi facilmente personalizzare la didascalia generata.
    Più tempo per la creatività: Automazione Didascalie ti libera dal compito noioso della scrittura delle didascalie, consentendoti di concentrarti sulla creazione di contenuti di qualità.

    ### Chi siamo:
    Siamo Alessandro e Riccardo, i creatori di Automazione Didascalie. Siamo appassionati di intelligenza artificiale e abbiamo sviluppato questa piattaforma per semplificare il processo di pubblicazione di foto sui social media per le aziende.

    Se desideri saperne di più su di noi o entrare in contatto, puoi visitare i nostri profili LinkedIn:

    [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/in/alessandro-goller/) **Alessandro**

    [![Linkedin](https://i.stack.imgur.com/gVE0j.png)](https://www.linkedin.com/in/ricci-riccardo/) **Riccardo**

    ### Prova le nostre altre funzionalità:
    Analisi avanzata delle immagini: Utilizza la nostra AI per ottenere informazioni dettagliate sul contenuto delle tue foto.
    Programmazione dei post: Pianifica e automatizza la pubblicazione dei tuoi contenuti sui social media.
    Non esitare a esplorare le varie funzionalità del nostro sito e a contattarci se hai domande o suggerimenti. Siamo qui per aiutarti a semplificare il processo di gestione dei tuoi contenuti sui social media!

    Grazie per aver scelto Automazione Didascalie. Speriamo che la nostra piattaforma renda il tuo lavoro più efficiente e creativo!

    """
)

if st.button("Premi per iniziare"):
    switch_page("action")
