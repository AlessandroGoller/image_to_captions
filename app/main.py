""" Main file """

import os
import subprocess
from datetime import datetime

from loguru import logger

log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logger.add(f"{log_folder}/{datetime.now().strftime('%Y-%m-%d')}.log", rotation="00:00")

# logger.debug("Questo è un messaggio di debug")
# logger.info("Questo è un messaggio informativo")
# logger.warning("Questo è un avvertimento")
# logger.error("Questo è un errore")
# logger.critical("Questo è un errore critico")

if __name__ == "__main__":
    subprocess.call(["streamlit", "run", "app/streamlit_app.py"])
