from typing import TypeVar, Generic
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.base import Base

model_table = TypeVar('model_table', bound=Base)


class BaseRepository(Generic[model_table]):
    """Базовый класс репозиторий"""

    ModelT: type[model_table]

    def __init__(self, async_session: AsyncSession):
        self.async_session = async_session

    async def add(self, values: dict):
        new_object = self.ModelT(**values)
        self.async_session.add(new_object)
        try:
            await self.async_session.commit()
        except SQLAlchemyError as sae:
            await self.async_session.rollback()
            raise sae
        return new_object

    async def get_all(self):
        query = select(self.ModelT)
        result = await self.async_session.execute(query)
        return result.scalars().all()

    async def get_by_id(self, id_: UUID | int):
        query = select(self.ModelT).where(self.ModelT.id == id_)
        result = await self.async_session.execute(query)
        return result.scalars().first()

    async def update_by_id(self, id_: UUID | int, values: dict):
        query = update(self.ModelT).where(self.ModelT.id == id_).values(**values).returning(self.ModelT)
        result = await self.async_session.execute(query)
        try:
            await self.async_session.commit()
        except SQLAlchemyError as sae:
            await self.async_session.rollback()
            raise sae
        return result.scalars().first()

    async def delete_one_by_id(self, id_: UUID | int):
        data = await self.get_by_id(id_)
        if data:
            await self.async_session.delete(data)
            try:
                await self.async_session.commit()
                return True
            except SQLAlchemyError as sae:
                await self.async_session.rollback()
                raise sae
        return False
