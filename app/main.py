""" Main file """

import os
import sys
from subprocess import call

from app.dependency import database_engine
from app.model import user, company
from app.utils.logger import configure_logger

logger = configure_logger()

def main()->None:
    """ Prepare DB """

    # user.database.metadata.create_all(bind=database_engine)
    company.database.metadata.create_all(bind=database_engine)

    # Activate Streamlit
    streamlit_path = os.path.abspath("app/streamlit_app.py")
    call(
        f"""{sys.executable} -m streamlit run {streamlit_path} \
            --server.headless=true --global.developmentMode=false""",
        shell=True,
        text=True,
    )

if __name__ == "__main__":
    main()
