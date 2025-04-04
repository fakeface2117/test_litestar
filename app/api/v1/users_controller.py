from litestar import Controller, get, post, put, patch, delete
from pydantic import UUID4

from app.api.v1.rest_models import User


class UserController(Controller):
    path = "/users"
    tags = ["users"]

    @post()
    async def create_user(self, data: User) -> User: ...  # data это обязательный параметр для post

    @get()
    async def list_users(self) -> list[User]: ...

    @patch(path="/{user_id:uuid}")
    async def partial_update_user(self, user_id: UUID4, data: User) -> User: ...

    @put(path="/{user_id:uuid}")
    async def update_user(self, user_id: UUID4, data: User) -> User: ...

    @get(path="/{user_id:uuid}")
    async def get_user(self, user_id: UUID4) -> User: ...

    @delete(path="/{user_id:uuid}")
    async def delete_user(self, user_id: UUID4) -> None: ...
