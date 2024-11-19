from sqlmodel import Field, SQLModel

from .base import TimestampMixin


class User(TimestampMixin, SQLModel, table=True):
    __tablename__ = 'users'

    id: int | None = Field(default=None, primary_key=True)

    phone_number: str = Field(max_length=11)
    password: str = Field(max_length=255)
