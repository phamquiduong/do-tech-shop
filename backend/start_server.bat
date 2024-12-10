@echo off

:: Start PostgreSQL Server
cd docker

if not exist .env (
    echo .env file does not exist. Creating from .env.example...
    copy .env.example .env
)

docker-compose up -d

cd ..


:: Install Python requirements
pip install -r requirements.txt


:: Migrate Database
call migrate.bat


:: Start Django server
echo --------------------------------
set /p PORT=Enter the Django server port (default: 8000):
if "%PORT%"=="" set PORT=8000

python manage.py runserver 127.0.0.1:%PORT%
