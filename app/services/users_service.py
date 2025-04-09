from litestar.plugins.sqlalchemy import repository
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.rest_models import UserCreate, User
from app.database.models import UsersTable
from app.repositories.users_repository import provide_users_repository


class UsersService:
    """Класс бизнес логики для пользователя"""
    def __init__(self, users_repo: repository.SQLAlchemyAsyncRepository):
        self.users_repo = users_repo

    async def create_user(self, user: UserCreate) -> User:
        created_user = await self.users_repo.add(UsersTable(**user.model_dump(exclude_unset=True)))
        await self.users_repo.session.commit()
        return User.model_validate(created_user)


async def get_users_service(db_session: AsyncSession) -> UsersService:
    users_repo = await provide_users_repository(db_session=db_session)
    return UsersService(users_repo)
