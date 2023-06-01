# image_to_captions

DESCRIPTION A package for doing great things!...

- https://image-to-caption.onrender.com/
- https://trello.com/b/BLyCd3Ju/kanban

- https://serpapi.com/dashboard
- https://dashboard.render.com/
- https://console.neon.tech/

## Informazioni generali
- divisorio utilizzato -> ;

- delete manually pywin32 from requirements-dev.txt -> it came from python-semantic-release
- pip version that works with pip-compile: python.exe -m pip install pip==23.0.1

## Angular commit
Type
Must be one of the following:

feat: A new feature
fix: A bug fix
docs: Documentation only changes
style: Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
refactor: A code change that neither fixes a bug nor adds a feature
perf: A code change that improves performance
test: Adding missing or correcting existing tests
chore: Changes to the build process or auxiliary tools and libraries such as documentation generation

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

## Poetry -> Todo
pip install poetry
### install from a file
poetry add --lock -r requirements.txt NON COSI

## Alembic
Questo comando crea un nuovo file di migrazione nella directory delle migrazioni specificata nel file di configurazione.
- alembic revision --autogenerate -m "descrizione della migrazione"

Se aggiunto un nuovo modello aggiungerlo nel file init dentro a model!!

Questo comando esegue tutte le migrazioni non ancora applicate al database, con head si intende tutte le migrazioni fino all'ultima creata.
- alembic upgrade head
- alembic downgrade NOME REVISIONE
- alembic downgrade -1

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


## Usage

- TODO

## Contributing

Interested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.

## License

`image_to_captions` was created by Alessandro Goller & Riccardo Ricci. It is licensed under the terms of the MIT license.

## Credits

