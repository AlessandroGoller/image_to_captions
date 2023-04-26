""" Main file """

import os
import subprocess
from datetime import datetime

from loguru import logger

log_folder = "log"
if not os.path.exists(log_folder):
    os.makedirs(log_folder)

logger.add(f"{log_folder}/{datetime.now().strftime('%Y-%m-%d')}.log", rotation="00:00")

def main()->None:
    """ Activate Streamlit """
    streamlit_path = os.path.abspath("app/streamlit_app.py")
    import sys
    subprocess.call(
        f"""{sys.executable} -m streamlit run {streamlit_path} \
            --server.headless=true --global.developmentMode=false""",
        shell=True,
        text=True,
    )

if __name__ == "__main__":
    main()
