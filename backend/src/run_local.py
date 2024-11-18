from settings import BASE_DIR
from utils.load_env import load_env

load_env(path=BASE_DIR / '../docker/.env')


def create_app():
    from main import app
    return app


app = create_app()
