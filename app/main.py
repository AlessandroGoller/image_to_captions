""" Main file """

import os
import sys
from subprocess import call

from app.utils.logger import configure_logger

logger = configure_logger()


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
