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


class UserCreate(BaseMappedModel):
    email: EmailStr
    name: str
    last_name: str
    birthday: date = Field(ge=date.fromisoformat('2000'))

    @field_validator('birthday')
    def check_birth_date(cls, value):
        if value >= datetime.now().date():
            raise ValueError('Не обманывайте, вы не из будущего')
        if date(year=value.year + 14, month=value.month, day=value.day) > datetime.now().date():
            raise ValueError('Вам должно быть 14 лет')
        return value
