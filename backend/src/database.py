import os

from sqlmodel import Session, create_engine


class DatabaseEngine:
    def __init__(self, url: str, *args, **kwargs) -> None:
        self.engine = create_engine(url=url, *args, **kwargs)

    @classmethod
    def from_config(cls, host: str, port: int | str, user: str, password: str, db_name: str):
        url = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}'
        return cls(url=url)


db_engine = DatabaseEngine.from_config(
    host='localhost',
    port=os.environ['POSTGRES_PORT'],
    user=os.environ['POSTGRES_USER'],
    password=os.environ['POSTGRES_PASSWORD'],
    db_name=os.environ['POSTGRES_DB'],
)


def get_session():
    with Session(db_engine.engine) as session:
        yield session
