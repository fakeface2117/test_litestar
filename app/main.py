from contextlib import asynccontextmanager

import uvicorn
from litestar import Litestar, get

from app.api.v1.user_controller import UserController

host = 'localhost'
port = 8080


@asynccontextmanager
async def lifespan(_app: Litestar):
    print('Start app')
    print(f'http://{host}:{port}/someapp/schema/swagger')
    yield
    print('Stop app')


@get('/')
async def index() -> str:
    return 'Hello World!'


app = Litestar(
    route_handlers=[index, UserController],
    path='/someapp',
    lifespan=[lifespan]
)

if __name__ == '__main__':
    uvicorn.run(app, host=host, port=port)
