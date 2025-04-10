from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.rest_models import UserCreate, User
from app.repositories.interface import BaseRepository
from app.repositories.users_repository import provide_users_repository


class UsersService:
    """Класс бизнес логики для пользователя"""
    def __init__(self, users_repo: BaseRepository):
        self.users_repo = users_repo

    async def create_user(self, user: UserCreate) -> User:
        created_user = await self.users_repo.add(user.model_dump(exclude_unset=True))
        return User.model_validate(created_user)


async def get_users_service(db_session: AsyncSession) -> UsersService:
    users_repo = provide_users_repository(async_session=db_session)
    return UsersService(users_repo)
