from sqlmodel import Session, select

from models import User as UserModel
from schemas.user import UserCreate
from utils.password import get_password_hash, verify_password


def get_user_by_id(session: Session, user_id: int) -> UserModel | None:
    return session.get(UserModel, user_id)


def get_user_by_phone_number(session: Session, phone_number: str) -> UserModel | None:
    statement = select(UserModel).where(UserModel.phone_number == phone_number)
    return session.exec(statement).first()


def authenticate_user(session: Session, phone_number: str, password: str) -> UserModel | None:
    user_db = get_user_by_phone_number(session=session, phone_number=phone_number)

    if not user_db:
        return None

    if not verify_password(password, user_db.password):
        return None

    return user_db


def create_user(session: Session, user_create: UserCreate) -> UserModel:
    hashed_password = get_password_hash(user_create.password)

    user_db = UserModel(
        phone_number=user_create.phone_number,
        password=hashed_password,
    )

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db
