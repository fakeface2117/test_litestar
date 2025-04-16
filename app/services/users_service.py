from uuid import UUID

from app.api.v1.users.rest_models import UserCreate, User, AllUsers, UserUpdate
from app.core.custom_logger import logger
from app.database.unit_of_work import AbstractUnitOfWork, UnitOfWork
from app.exceptions.exceptions import UserNotFoundException, UsersNotFoundException


class UsersService:
    """Класс бизнес логики для пользователя"""
    def __init__(self, uow: AbstractUnitOfWork):
        self.uow = uow

    async def create_user(self, user: UserCreate) -> User:
        async with self.uow:
            created_user = await self.uow.users.add(user.model_dump(exclude_unset=True))
            await self.uow.commit()
        return User.model_validate(created_user)

    async def get_user(self, user_id: UUID) -> User:
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            if not user:
                logger.warning(f'User with id {user_id} not found in database')
                raise UserNotFoundException(user_id)
            return User.model_validate(user)

    async def get_all_users(self) -> AllUsers:
        async with self.uow:
            all_users = await self.uow.users.get_all()
            if not all_users:
                raise UsersNotFoundException
            return AllUsers(users=[User.model_validate(user) for user in all_users])

    async def update_user_by_id(self, user_id: UUID, user: UserUpdate) -> User:
        async with self.uow:
            updated_user = await self.uow.users.update_by_id(user_id, user.model_dump(exclude_none=True))
            await self.uow.commit()
            return User.model_validate(updated_user)

    async def delete_user(self, user_id: UUID) -> None:
        async with self.uow:
            delete_result = await self.uow.users.delete_one_by_id(user_id)
            if not delete_result:
                logger.warning(f'User with id {user_id} not found in database')
                raise UserNotFoundException(user_id)
            await self.uow.commit()


async def get_users_service() -> UsersService:
    uow = UnitOfWork()
    return UsersService(uow)
