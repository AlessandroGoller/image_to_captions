echo "Installing dev dependencies"

pip install -r requirements.txt
echo "pip install -r requirements-dev.txt"

echo "ruff"
ruff app || goto :error

echo "Run type checking"
mypy app --exclude custom_logging.py --exclude main.py|| goto :error

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