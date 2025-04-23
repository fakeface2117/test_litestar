from uuid import UUID

from app.api.v1.cars.rest_models import Car, CarCreate, AllUserCars, AllCars
from app.core.custom_logger import logger
from app.database.unit_of_work import AbstractUnitOfWork, UnitOfWork
from app.exceptions.exceptions import UserCarsNotFoundException, CarNotFoundException, CarsNotFoundException


class CarsService:
    """Класс для автомобилей"""

    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def add_car(self, car: CarCreate) -> Car:
        async with self.uow:
            new_car = await self.uow.cars.add(car.model_dump(exclude_unset=True))
            await self.uow.commit()
        return Car.model_validate(new_car)

    async def get_user_cars(self, user_id: UUID) -> AllUserCars:
        async with self.uow:
            all_user_cars = await self.uow.cars.get_by_filters({'car_owner': user_id})
            if not all_user_cars:
                raise UserCarsNotFoundException(user_id)
            return AllUserCars(cars=[Car.model_validate(row) for row in all_user_cars])

    async def get_all_cars(self) -> AllCars:
        async with self.uow:
            all_cars = await self.uow.cars.get_all()
            if not all_cars:
                raise CarsNotFoundException
            return AllCars(cars=[Car.model_validate(row) for row in all_cars])

    async def delete_car(self, user_id: UUID, car_id: UUID) -> None:
        async with self.uow:
            delete_result = await self.uow.cars.delete_by_filters({'id': car_id, 'car_owner': user_id})
            if not delete_result:
                logger.warning(f'Car with id {car_id} not found for user {user_id}')
                raise CarNotFoundException(car_id, user_id)
            await self.uow.commit()


async def get_cars_service() -> CarsService:
    uow = UnitOfWork()
    return CarsService(uow)
