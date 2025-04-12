from litestar import Router
from litestar.di import Provide

from app.api.v1.users.users_controller import UserController, OtherController
from app.database.connection import get_async_session

v1_router = Router(
    route_handlers=[UserController, OtherController],
    path="/api/v1",
    dependencies={'db_session': Provide(get_async_session)}
)
