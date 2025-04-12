from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.rest_models import UserCreate, User, AllUsers, UserUpdate
from app.repositories.interface import BaseRepository
from app.repositories.users_repository import provide_users_repository


class UsersService:
    """Класс бизнес логики для пользователя"""

    def __init__(self, users_repo: BaseRepository):
        self.users_repo = users_repo

    async def create_user(self, user: UserCreate) -> User:
        created_user = await self.users_repo.add(user.model_dump(exclude_unset=True))
        return User.model_validate(created_user)

    async def get_user(self, user_id: UUID) -> User:
        user = await self.users_repo.get_by_id(user_id)
        return User.model_validate(user)

    async def get_all_users(self) -> AllUsers:
        users = await self.users_repo.get_all()
        return AllUsers(users=[User.model_validate(user) for user in users])

    async def update_user_by_id(self, user_id: UUID, user: UserUpdate) -> User:
        updated_user = await self.users_repo.update_by_id(user_id, user.model_dump(exclude_none=True))
        return User.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> None:
        delete_result = await self.users_repo.delete_one_by_id(user_id)
        if not delete_result:
            raise


async def get_users_service(db_session: AsyncSession) -> UsersService:
    users_repo = provide_users_repository(async_session=db_session)
    return UsersService(users_repo)
