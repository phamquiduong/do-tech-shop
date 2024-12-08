@echo off
:: Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Error occurred while installing dependencies. Please check.
    exit /b 1
)

:: Run the migration script
echo Running migrations...
call migrate.bat
if %errorlevel% neq 0 (
    echo Error occurred during migrations. Please check.
    exit /b 1
)

:: Start the Django development server
echo Starting the Django development server...
python manage.py runserver
if %errorlevel% neq 0 (
    echo Error occurred while starting the development server. Please check.
    exit /b 1
)
