from contextlib import asynccontextmanager

import uvicorn
from litestar import Litestar, get
from litestar.datastructures import State
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    base
)

from app.api.v1.users_controller import base_router
from app.core.config import settings


@asynccontextmanager
async def lifespan(_app: Litestar):
    print('Start app')
    print(f'http://{settings.DB_HOST}:{settings.DB_PORT}/someapp/schema/swagger')
    _app.state.some_value1 = 'value1'  # передача параметра в стейт
    yield
    print('Stop app')


session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
    connection_string=settings.DB_CONNECTION_STRING, session_config=session_config
)  # Create 'db_session' dependency.
sqlalchemy_plugin = SQLAlchemyInitPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    """Initializes the database."""
    async with sqlalchemy_config.get_engine().begin() as conn:
        await conn.run_sync(base.UUIDBase.metadata.create_all)


@get('/')
async def index() -> str:
    return 'Hello World!'


app = Litestar(
    route_handlers=[index, base_router],
    path='/someapp',
    on_startup=[on_startup],
    lifespan=[lifespan],
    plugins=[SQLAlchemyInitPlugin(config=sqlalchemy_config)],
    state=State({'some_value2': 'value2'}, deep_copy=True)
)

if __name__ == '__main__':
    uvicorn.run(app, host=settings.DB_HOST, port=settings.DB_PORT)
