from litestar.plugins.sqlalchemy import repository
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UsersTable


class UsersRepository(repository.SQLAlchemyAsyncRepository[UsersTable]):
    """Класс репозиторий для пользователя"""
    model_type = UsersTable


async def provide_users_repository(db_session: AsyncSession) -> UsersRepository:
    return UsersRepository(session=db_session)
