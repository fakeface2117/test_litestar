from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import UsersTable
from app.repositories.interface import BaseRepository


class UsersRepository(BaseRepository[UsersTable]):
    """Класс репозиторий для пользователя"""
    ModelT = UsersTable

    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session)
        self.async_session = async_session
