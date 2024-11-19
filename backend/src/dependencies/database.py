from sqlmodel import Session

from database import db_engine


def get_session():
    with Session(db_engine.engine) as session:
        yield session
