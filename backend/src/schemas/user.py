import re

from pydantic import BaseModel, ConfigDict, Field, field_validator

from constants.user import PHONE_NUMBER_REGEX


class UserInfo(BaseModel):
    id: int
    phone_number: str

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'id': 1,
                    'phone_number': '0987654321',
                }
            ]
        }
    )


class UserLogin(BaseModel):
    phone_number: str
    password: str = Field(min_length=8)

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, value):
        if not re.match(PHONE_NUMBER_REGEX, value):
            raise ValueError("Invalid phone number format.")
        return value

    @field_validator('password')
    @classmethod
    def validate_password(cls, value):
        if not re.search(r'[a-z]', value):
            raise ValueError("Password must contain at least one lowercase letter.")
        if not re.search(r'[A-Z]', value):
            raise ValueError("Password must contain at least one uppercase letter.")
        if not re.search(r'\d', value):
            raise ValueError("Password must contain at least one digit.")
        if not re.search(r'[^a-zA-Z0-9]', value):
            raise ValueError("Password must contain at least one special character.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            'examples': [
                {
                    'phone_number': '0987654321',
                    'password': 'Pass@123'
                }
            ]
        }
    )


class UserCreate(UserLogin):
    pass
