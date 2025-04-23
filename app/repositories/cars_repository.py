from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import CarsTable
from app.repositories.interface import BaseRepository


class CarsRepository(BaseRepository[CarsTable]):
    """Класс репозиторий для автомобилей пользователя"""
    ModelT = CarsTable

    def __init__(self, async_session: AsyncSession):
        super().__init__(async_session)
        self.async_session = async_session
