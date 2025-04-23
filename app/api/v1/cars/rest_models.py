from datetime import date, datetime
from typing import Any
from uuid import UUID

from pydantic import model_validator

from app.api.v1.base_schema import BaseMappedModel


class Car(BaseMappedModel):
    id: UUID | None
    car_brand: str
    car_model: str
    car_year: int
    car_owner: UUID
    purchase_date: date
    in_stock: bool


class CarValidatedSchema(BaseMappedModel):
    @model_validator(mode='before')
    @classmethod
    def validate_sums(cls, data: Any):
        if isinstance(data, dict):
            car_year = data.get('car_year')
            if car_year > datetime.now().year:
                raise ValueError('Автомобиль не может быть моложе текущего года')
            try:
                purchase_date: date = datetime.strptime(data.get('purchase_date'), '%Y-%m-%d').date()
            except ValueError:
                raise ValueError("Invalid date format. Use YYYY-MM-DD.")
            if purchase_date.year < car_year:
                raise ValueError('Дата покупки не может быть меньше года выпуска авто')
            return data


class CarCreate(CarValidatedSchema):
    car_brand: str
    car_model: str
    car_year: int
    car_owner: UUID
    purchase_date: date
    in_stock: bool | None = None


class CarUpdate(BaseMappedModel):
    in_stock: bool | None = None


class AllUserCars(BaseMappedModel):
    cars: list[Car]


class AllCars(BaseMappedModel):
    cars: list[Car]
