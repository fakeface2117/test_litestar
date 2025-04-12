from typing import Annotated

from litestar import Controller, get, post, put, patch, delete, route, HttpMethod, Router
from litestar.datastructures import ImmutableState
from litestar.di import Provide
from litestar.params import Parameter
from pydantic import UUID4

from app.api.v1.users.rest_models import User, UserCreate
from app.services.users_service import get_users_service, UsersService


class UserController(Controller):
    path = "/users"
    tags = ["users"]

    dependencies = {'user_service': Provide(get_users_service)}

    @post()
    async def create_user(self, data: UserCreate, user_service: UsersService) -> User:
        return await user_service.create_user(data)

    @get()
    async def list_users(self, state: ImmutableState) -> dict:  # Передача стейта. Можно с State
        return state.dict()

    @patch(path="/{user_id:uuid}")
    async def partial_update_user(self, user_id: UUID4, data: User) -> User: ...

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: User) -> User: ...

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> User: ...

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> None: ...


annotated_parameter = Annotated[int, Parameter(ge=1, le=10, description='Описание параметра', title='Some index')]


class OtherController(Controller):
    # просто потестить
    path = "/other"
    tags = ["other"]

    @route(path="/some-path", http_method=[HttpMethod.GET, HttpMethod.POST])
    async def my_endpoint(self) -> None: ...

    @route(path="/other-path/{index:int}", http_method=[HttpMethod.GET])
    async def other_endpoint(self, index: annotated_parameter) -> dict[str, int]:
        return {'my_index': index}



