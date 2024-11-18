from fastapi import FastAPI

from settings import BASE_DIR
from utils.load_env import load_env

load_env(path=BASE_DIR / '../docker/.env')

app = FastAPI()
