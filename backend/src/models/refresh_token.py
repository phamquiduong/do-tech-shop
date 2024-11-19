from sqlmodel import Field, SQLModel

from .base import TimestampMixin


class RefreshToken(TimestampMixin, SQLModel, table=True):
    __tablename__ = 'refresh_tokens'

    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key='users.id', ondelete='CASCADE')
