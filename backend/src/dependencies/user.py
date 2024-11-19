from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from dependencies.database import get_session
from models.user import User as UserModel
from schemas.token import oauth2_scheme
from services.token import get_user_from_access_token


async def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> UserModel:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    user = get_user_from_access_token(session=session, access_token=token)

    if user is None:
        raise credentials_exception

    return user
