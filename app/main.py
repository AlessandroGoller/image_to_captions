""" Main file """

import os
import subprocess
from datetime import datetime

from loguru import logger

log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logger.add(f"{log_folder}/{datetime.now().strftime('%Y-%m-%d')}.log", rotation="00:00")


if __name__ == "__main__":
    subprocess.call(["streamlit", "run", "app/streamlit_app.py"])
