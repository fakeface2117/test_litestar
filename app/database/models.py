import os
from datetime import datetime, date
from uuid import UUID

from dotenv import load_dotenv
from litestar.plugins.sqlalchemy import base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../.env'))


class UsersTable(base.UUIDBase):
    """Владельцы машин"""
    __tablename__ = 'users'
    email: Mapped[str]
    name: Mapped[str]
    last_name: Mapped[str]
    birthday: Mapped[date]

    cars: Mapped[list['CarsTable']] = relationship('CarsTable', back_populates='user')


class CarsTable(base.UUIDBase):
    """Машины пользователей"""
    __tablename__ = 'cars'
    car_brand: Mapped[str]
    car_model: Mapped[str]
    car_year: Mapped[int]
    car_owner: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    purchase_date: Mapped[datetime]
    in_stock: Mapped[bool] = mapped_column(default=True)

    user: Mapped['UsersTable'] = relationship(UsersTable, back_populates='cars')
    fixes: Mapped[list['CarsFixesTable']] = relationship('CarsFixesTable', back_populates='car')
    photos: Mapped[list['CarsPhotosTable']] = relationship('CarsPhotosTable', back_populates='car')


class CarsPhotosTable(base.BigIntBase):
    """Фото машин"""
    __tablename__ = 'cars_photos'
    car_id: Mapped[UUID] = mapped_column(ForeignKey('cars.id'))
    photo_filename: Mapped[str]

    car: Mapped['CarsTable'] = relationship('CarsTable', back_populates='photos')


class CarsFixesTable(base.BigIntBase):
    """Поломки машин, причины и восстановление"""
    __tablename__ = 'cars_fixes'
    car_id: Mapped[UUID] = mapped_column(ForeignKey('cars.id'))
    crash_date: Mapped[datetime]
    crash_reason: Mapped[str]
    fix_date: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    fix_price: Mapped[int]

    car: Mapped['CarsTable'] = relationship('CarsTable', back_populates='fixes')
