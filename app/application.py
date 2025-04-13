from contextlib import asynccontextmanager

from litestar import Litestar
from litestar.datastructures import State

from app.api.v1.base_router import v1_router
from app.core.config import settings
from app.database.connection import create_db


@asynccontextmanager
async def lifespan(_app: Litestar):
    print('Start app')
    print(settings.SERVICE_SWAGGER_URL)
    _app.state.some_value1 = 'value1'  # передача параметра в стейт
    yield
    print('Stop app')


async def on_startup() -> None:
    """Initializes the database."""
    await create_db()


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[v1_router],
        path=settings.SERVICE_BASE_URL,
        lifespan=[lifespan],
        on_startup=[on_startup],
        state=State({'some_value2': 'value2'}, deep_copy=True)
    )
