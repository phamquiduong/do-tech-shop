@echo off
:: Navigate to the 'src' directory
cd src
if %errorlevel% neq 0 (
    echo The 'src' directory does not exist. Please check.
    exit /b 1
)

:: Run the 'makemigrations' command
echo Running makemigrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Error occurred while running makemigrations. Please check.
    exit /b 1
)

:: Run the 'migrate' command
echo Running migrate...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Error occurred while running migrate. Please check.
    exit /b 1
)

echo Migrations completed successfully!
