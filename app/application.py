from contextlib import asynccontextmanager

from litestar import Litestar

from app.api.v1.base_router import v1_router
from app.core.config import settings
from app.core.custom_logger import logger
from app.database.connection import create_db
from app.exceptions.exceptions_handlers import exception_handlers


@asynccontextmanager
async def lifespan(_app: Litestar):
    logger.info(f'Swagger url: {settings.SERVICE_SWAGGER_URL}')
    yield
    logger.info('Stopping app')


async def on_startup() -> None:
    await create_db()


def create_app() -> Litestar:
    return Litestar(
        route_handlers=[v1_router],
        path=settings.SERVICE_BASE_URL,
        lifespan=[lifespan],
        on_startup=[on_startup],
        exception_handlers=exception_handlers
    )
