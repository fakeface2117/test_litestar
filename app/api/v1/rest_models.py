from datetime import date
from uuid import UUID

from pydantic import BaseModel, EmailStr, ConfigDict


class BaseMappedModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True
    )


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
