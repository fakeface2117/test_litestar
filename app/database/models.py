from datetime import datetime, date
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from app.database.base import Base


class UsersTable(Base):
    """Владельцы машин"""
    __tablename__ = 'users'
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    email: Mapped[str]
    name: Mapped[str]
    last_name: Mapped[str]
    birthday: Mapped[date]

    cars: Mapped[list['CarsTable']] = relationship('CarsTable', back_populates='user')


class CarsTable(Base):
    """Машины пользователей"""
    __tablename__ = 'cars'
    id: Mapped[UUID] = mapped_column(default=uuid4, primary_key=True)
    car_brand: Mapped[str]
    car_model: Mapped[str]
    car_year: Mapped[int]
    car_owner: Mapped[UUID] = mapped_column(ForeignKey('users.id'))
    purchase_date: Mapped[datetime]
    in_stock: Mapped[bool] = mapped_column(default=True)

    user: Mapped['UsersTable'] = relationship(UsersTable, back_populates='cars')
    fixes: Mapped[list['CarsFixesTable']] = relationship('CarsFixesTable', back_populates='car')
    photos: Mapped[list['CarsPhotosTable']] = relationship('CarsPhotosTable', back_populates='car')


class CarsPhotosTable(Base):
    """Фото машин"""
    __tablename__ = 'cars_photos'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    car_id: Mapped[UUID] = mapped_column(ForeignKey('cars.id'))
    photo_filename: Mapped[str]

    car: Mapped['CarsTable'] = relationship('CarsTable', back_populates='photos')


class CarsFixesTable(Base):
    """Поломки машин, причины и восстановление"""
    __tablename__ = 'cars_fixes'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    car_id: Mapped[UUID] = mapped_column(ForeignKey('cars.id'))
    crash_date: Mapped[datetime]
    crash_reason: Mapped[str]
    fix_date: Mapped[datetime | None] = mapped_column(nullable=True, default=None)
    fix_price: Mapped[int]

    car: Mapped['CarsTable'] = relationship('CarsTable', back_populates='fixes')
