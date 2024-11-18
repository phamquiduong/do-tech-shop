from dotenv import load_dotenv
from dotenv.main import StrPath


def load_env(path: StrPath):
    if not load_dotenv(dotenv_path=path):
        raise FileNotFoundError(f"No.env file found in {path}")
