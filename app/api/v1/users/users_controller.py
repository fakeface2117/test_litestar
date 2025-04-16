from typing import Annotated

from litestar import Controller, get, post, patch, delete, route, HttpMethod
from litestar.di import Provide
from litestar.params import Parameter
from pydantic import UUID4

from app.api.v1.users.rest_models import User, UserCreate, AllUsers, UserUpdate
from app.services.users_service import get_users_service, UsersService


class UserController(Controller):
    path = "/users"
    tags = ["users"]

    dependencies = {'user_service': Provide(get_users_service)}

    @post('/')
    async def create_user(self, data: UserCreate, user_service: UsersService) -> User:
        return await user_service.create_user(data)

    @get('/')
    async def list_users(self, user_service: UsersService) -> AllUsers:
        return await user_service.get_all_users()

    @patch(path="/{user_id:uuid}")
    async def partial_update_user(self, user_id: UUID4, data: UserUpdate, user_service: UsersService) -> User:
        return await user_service.update_user_by_id(user_id, data)

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4, user_service: UsersService) -> User:
        return await user_service.get_user(user_id)

    @delete(path="/{user_id:uuid}", status_code=204)
    async def delete_user(self, user_id: UUID4, user_service: UsersService) -> None:
        return await user_service.delete_user(user_id)


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
