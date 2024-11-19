from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from dependencies.database import get_session
from dependencies.user import get_current_user
from models.user import User as UserModel
from schemas.token import AccessRefreshToken, AccessToken, FastAPIAcessToken, RefreshTokenRequest, TokenData
from schemas.user import UserCreate, UserInfo, UserLogin
from services.token import (create_refresh_token, generate_access_token, generate_refresh_token,
                            get_user_from_refresh_token)
from services.user import authenticate_user, create_user, get_user_by_phone_number

router = APIRouter(prefix='/auth', tags=['Authentication'])


@router.post('/register', status_code=status.HTTP_201_CREATED)
async def register_new_user(
    session: Annotated[Session, Depends(get_session)],
    user_create: UserCreate = Body()
) -> UserInfo:
    if get_user_by_phone_number(session=session, phone_number=user_create.phone_number):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this phone number already exists",
        )

    user_db = create_user(session=session, user_create=user_create)

    return UserInfo(**user_db.model_dump())


@router.post('/login')
async def login_user(
    session: Annotated[Session, Depends(get_session)],
    user_login: UserLogin = Body()
) -> AccessRefreshToken:
    user_db = authenticate_user(session=session, phone_number=user_login.phone_number, password=user_login.password)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, access_exp = generate_access_token(user_db=user_db)

    refresh_token_db = create_refresh_token(session=session, user_db=user_db)
    refresh_token, refresh_exp = generate_refresh_token(refresh_token_db=refresh_token_db)

    return AccessRefreshToken(
        access_token=TokenData(token=access_token, exp=access_exp),
        refresh_token=TokenData(token=refresh_token, exp=refresh_exp)
    )


@router.post('/refresh_token')
async def generate_access_token_from_refresh_token(
    session: Annotated[Session, Depends(get_session)],
    refresh_token_request: RefreshTokenRequest = Body()
) -> AccessToken:
    user_db = get_user_from_refresh_token(session=session, refresh_token=refresh_token_request.refresh_token)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Expired or invalid refresh token",
        )

    access_token, access_exp = generate_access_token(user_db=user_db)
    return AccessToken(
        access_token=TokenData(token=access_token, exp=access_exp)
    )


@router.post("/token", include_in_schema=False)
async def login_for_access_token(
    session: Annotated[Session, Depends(get_session)],
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> FastAPIAcessToken:
    user_db = authenticate_user(session=session, phone_number=form_data.username, password=form_data.password)

    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token, _ = generate_access_token(user_db=user_db)
    return FastAPIAcessToken(access_token=access_token, token_type="bearer")


@router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[UserModel, Depends(get_current_user)],
) -> UserInfo:
    return UserInfo(**current_user.model_dump())
