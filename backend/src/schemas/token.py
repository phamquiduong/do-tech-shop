from datetime import datetime

from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


class FastAPIAcessToken(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class TokenData(BaseModel):
    token: str
    exp: datetime


class AccessRefreshToken(BaseModel):
    access_token: TokenData
    refresh_token: TokenData


class AccessToken(BaseModel):
    access_token: TokenData


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessTokenPayload(BaseModel):
    user_id: int
    exp: datetime


class RefreshTokenPayload(BaseModel):
    refresh_token_id: int
    exp: datetime
