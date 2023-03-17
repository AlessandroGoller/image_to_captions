echo "Installing dev dependencies"
FOR /F "tokens=* USEBACKQ" %%F IN (`aws codeartifact get-authorization-token --domain kwantis-pypi --domain-owner 857010180973 --query authorizationToken --output text`) DO (
SET CODEARTIFACT_AUTH_TOKEN=%%F
)

pip install -r requirements.txt
pip install --index-url https://aws:%CODEARTIFACT_AUTH_TOKEN%@kwantis-pypi-857010180973.d.codeartifact.eu-central-1.amazonaws.com/pypi/kwantis-pypi-repository/simple/ --extra-index-url https://pypi.org/simple -r requirements-kwantis.txt
pip install -r requirements-dev.txt

echo "RUFF"
ruff app || goto :error

echo "Run pylint"
pylint app || goto :error

echo "Run type checking"
mypy --install-types --non-interactive app || goto :error

echo "Running tests"
coverage run --source=app -m pytest || goto :error
ECHO "Create HTML Coverage report"
coverage html || goto :error
ECHO "Coverage report"
coverage report --show-missing --skip-covered --skip-empty --omit="*test*,*exception*" || goto :error
goto :end

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

:end
echo Pipeline run succesfully
