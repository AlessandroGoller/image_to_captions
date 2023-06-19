""" Main file """

import os
import sys
from subprocess import call

from app.utils.logger import configure_logger

logger = configure_logger()
import subprocess

import multiprocessing
import subprocess
import sys
import time

# Funzione per avviare FastAPI
def start_fastapi():
    fastapi_path = "app/main_fastapi.py"
    fastapi_command = f"{sys.executable} env/Scripts/uvicorn app/main_fastapi:app --reload --port 5000"
    # fastapi_command = f"{sys.executable} {fastapi_path}"
    subprocess.run(fastapi_command, shell=True)

# Funzione per avviare Streamlit
def start_streamlit():
    streamlit_path = "app/Homepage.py"
    streamlit_command = f"{sys.executable} -m streamlit run {streamlit_path} --server.headless=true --global.developmentMode=false"
    # subprocess.run(streamlit_command, shell=True)

def main_old() -> None:
    """ Start the systems """

    # Avvia FastAPI e Streamlit come processi separati
    fastapi_process = multiprocessing.Process(target=start_fastapi)
    streamlit_process = multiprocessing.Process(target=start_streamlit)

    fastapi_process.start()
    streamlit_process.start()

    # Attendi la terminazione dei processi
    # fastapi_process.join()
    # streamlit_process.join()

    # Attendi 5 secondi
    time.sleep(5)

    # Termina i processi
    fastapi_process.terminate()
    streamlit_process.terminate()

def main() -> None:
    """Prepare DB"""

    # Activate Streamlit
    streamlit_path = os.path.abspath("app/Homepage.py")
    call(
        f"""{sys.executable} -m streamlit run {streamlit_path} \
            --server.headless=true --global.developmentMode=false""",
        shell=True,
        text=True,
    )



if __name__ == "__main__":
    main()
