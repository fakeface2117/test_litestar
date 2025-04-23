from litestar import Router

from app.api.v1.cars.cars_controller import CarsController
from app.api.v1.users.users_controller import UserController, OtherController

v1_router = Router(
    route_handlers=[UserController, OtherController, CarsController],
    path="/api/v1"
)
