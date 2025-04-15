from litestar import Router

from app.api.v1.users.users_controller import UserController, OtherController

v1_router = Router(
    route_handlers=[UserController, OtherController],
    path="/api/v1"
)
