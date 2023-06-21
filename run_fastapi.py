""" Module for run Main from the principal folder, streamlit share needs it """

import multiprocessing
import subprocess
import sys

from app.utils.logger import configure_logger

logger = configure_logger()

# Funzione per avviare FastAPI
def start_fastapi()-> None:
    """ Start FastApi module """
    fastapi_command = f"{sys.executable} -m uvicorn app.main_fastapi:app --host 0.0.0.0 --port 80"
    subprocess.run(fastapi_command, shell=True, check=False)

if __name__ == "__main__":
    # Avvia FastAPI e Streamlit come processi separati
    fastapi_process = multiprocessing.Process(target=start_fastapi)
    #streamlit_process =  multiprocessing.Process(target=main)

    fastapi_process.start()
    #streamlit_process.start()

    # Attendi la terminazione dei processi / fastapi_process.join()
    fastapi_process.join()
    #streamlit_process.join()

    # Attendi 5 secondi
    #time.sleep(5)

    # Termina i processi
    #fastapi_process.terminate()
    #streamlit_process.terminate()
