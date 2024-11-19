from datetime import datetime, timedelta, timezone

import jwt
from sqlmodel import Session

from models.refresh_token import RefreshToken as RefreshTokenModel
from models.user import User as UserModel
from schemas.token import AccessTokenPayload, RefreshTokenPayload
from services.user import get_user_by_id
from settings import ACCESS_TOKEN_EXPIRE_TIME, ALGORITHM, REFRESH_TOKEN_EXPIRE_TIME, SECRET_KEY


def create_refresh_token(session: Session, user_db: UserModel) -> RefreshTokenModel:
    refresh_token = RefreshTokenModel(user_id=user_db.id)  # type: ignore

    session.add(refresh_token)
    session.commit()
    session.refresh(refresh_token)

    return refresh_token


def get_refresh_token(session: Session, refresh_token_id: int):
    return session.get(RefreshTokenModel, refresh_token_id)


def generate_access_token(
    user_db: UserModel,
    expires_delta: timedelta = ACCESS_TOKEN_EXPIRE_TIME
) -> tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + expires_delta

    payload = AccessTokenPayload(
        user_id=user_db.id,    # type: ignore
        exp=expire
    )

    encoded_jwt = jwt.encode(payload=payload.model_dump(), key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt, expire


def generate_refresh_token(
    refresh_token_db: RefreshTokenModel,
    expires_delta: timedelta = REFRESH_TOKEN_EXPIRE_TIME
) -> tuple[str, datetime]:
    expire = datetime.now(timezone.utc) + expires_delta

    payload = RefreshTokenPayload(
        refresh_token_id=refresh_token_db.id,   # type: ignore
        exp=expire
    )

    encoded_jwt = jwt.encode(payload=payload.model_dump(), key=SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt, expire


def get_user_from_access_token(session: Session, access_token: str) -> UserModel | None:
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        access_token_payload = AccessTokenPayload(**payload)

        user_id = access_token_payload.user_id
        return get_user_by_id(session=session, user_id=user_id)
    except jwt.InvalidTokenError:
        return None


def get_user_from_refresh_token(session: Session, refresh_token: str) -> UserModel | None:
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        refresh_token_payload = RefreshTokenPayload(**payload)

        refresh_token_id = refresh_token_payload.refresh_token_id
        refresh_token_db = get_refresh_token(session=session, refresh_token_id=refresh_token_id)

        if not refresh_token_db:
            return None

        user_id = refresh_token_db.user_id
        return get_user_by_id(session=session, user_id=user_id)

    except jwt.InvalidTokenError:
        return None
