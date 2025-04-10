from datetime import date
from uuid import UUID

from pydantic import EmailStr

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
    birthday: date
