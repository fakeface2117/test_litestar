from litestar import Controller, get, post, delete
from litestar.di import Provide
from pydantic import UUID4

from app.api.v1.cars.rest_models import CarCreate, Car, AllCars, AllUserCars
from app.services.cars_service import get_cars_service, CarsService


class CarsController(Controller):
    path = "/cars"
    tags = ["cars"]

    dependencies = {'cars_service': Provide(get_cars_service)}

    @post('/')
    async def create_car(self, data: CarCreate, cars_service: CarsService) -> Car:
        return await cars_service.add_car(data)

    @get('/')
    async def list_all_cars(self, cars_service: CarsService) -> AllCars:
        return await cars_service.get_all_cars()

    @get(path="/{user_id:uuid}")
    async def get_user_cars(self, user_id: UUID4, cars_service: CarsService) -> AllUserCars:
        return await cars_service.get_user_cars(user_id)

    @delete(path="/{user_id:uuid}", status_code=204)
    async def delete_car(self, user_id: UUID4, car_id: UUID4, cars_service: CarsService) -> None:
        return await cars_service.delete_car(user_id=user_id, car_id=car_id)
