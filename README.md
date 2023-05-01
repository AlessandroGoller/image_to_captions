# image_to_captions
- https://image-to-caption.onrender.com/
- https://trello.com/b/BLyCd3Ju/kanban

- https://serpapi.com/dashboard
- https://dashboard.render.com/
- https://console.neon.tech/

## Informazioni generali
- divisorio utilizzato -> ;

## Add library
pip freeze > requirements-dev.in
pip-compile

## logging
from app.utils.logger import configure_logger
logger = configure_logger()

logger.info("Write here)
logger.debug
logger.warn
logger.error
logger.fatal

# Technology:
- sphinx: Documentation
- Alembic: Migration DB
- Sqlalchemy: ORM DB
- Logging: Loguru
- FE: streamlit (only for demo)

# Structure:
The repository is structured around the following folders: config, services, test, utils, and log.

## Config
The config folder likely contains configuration files and settings that are used by the services and utilities within the repository. These files may be used to define things like database connection strings, application settings, or other important parameters that are required by the code base.

## Services
The services folder is likely where most of the core functionality of the repository will be located. This may include code that performs actual calculations or data processing, as well as code that interfaces with external systems or APIs.

## Test
The test folder is likely where unit tests for the repository live. These tests are designed to validate the functionality of the code and catch any bugs or errors before the code is deployed to production.

## Utils
The utils folder contains any utility code that doesn't fit into one of the other folders. This could include common functions or helpers that are used throughout the repository, or even code that is shared across multiple projects within an organization.

## Log
Finally, the log folder likely houses log files generated by the repository. These files may contain information about errors, warnings, or other events that have occurred within the code, and are used to help debug issues and diagnose problems that are encountered by users.
