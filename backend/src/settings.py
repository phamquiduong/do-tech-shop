from datetime import timedelta
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# JWT authentication
SECRET_KEY = 'not-secret-key'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_TIME = timedelta(minutes=15)
REFRESH_TOKEN_EXPIRE_TIME = timedelta(days=60)
