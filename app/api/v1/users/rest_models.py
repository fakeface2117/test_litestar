from datetime import date, datetime
from uuid import UUID

from pydantic import EmailStr, Field, field_validator

from app.api.v1.base_schema import BaseMappedModel


class User(BaseMappedModel):
    id: UUID | None
    email: EmailStr
    name: str
    last_name: str
    birthday: date


class UserValidatedSchema(BaseMappedModel):
    birthday: date

    @field_validator('birthday')
    def check_birth_date(cls, value):
        if value > datetime.now().date():
            raise ValueError('Не обманывайте, вы не из будущего')
        if date(year=value.year + 14, month=value.month, day=value.day) > datetime.now().date():
            raise ValueError('Вам должно быть 14 лет')
        return value


class UserCreate(UserValidatedSchema):
    email: EmailStr
    name: str = Field(max_length=100)
    last_name: str = Field(max_length=100)
    birthday: date


class UserUpdate(BaseMappedModel):
    name: str | None = Field(max_length=100, default=None)
    last_name: str | None = Field(max_length=100, default=None)
    birthday: date | None = None


class AllUsers(BaseMappedModel):
    users: list[User]
