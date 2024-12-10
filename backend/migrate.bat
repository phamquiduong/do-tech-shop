@echo off

cd src

:: Create migrations
python manage.py makemigrations

:: Apply migrations
python manage.py migrate

echo Migrations completed successfully!
