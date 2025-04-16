from uuid import UUID

from app.api.v1.users.rest_models import UserCreate, User, AllUsers, UserUpdate
from app.core.custom_logger import logger
from app.database.unit_of_work import AbstractUnitOfWork
from app.exceptions.exceptions import UserNotFoundException


class UsersService:
    """Класс бизнес логики для пользователя"""

    async def create_user(self, uow: AbstractUnitOfWork, user: UserCreate) -> User:
        async with uow:
            created_user = await uow.users.add(user.model_dump(exclude_unset=True))
            await uow.commit()
        return User.model_validate(created_user)

    async def get_user(self, uow: AbstractUnitOfWork, user_id: UUID) -> User:
        async with uow:
            user = await uow.users.get_by_id(user_id)
            if not user:
                logger.warning(f'User with id {user_id} not found in database')
                raise UserNotFoundException(user_id)
            return User.model_validate(user)

    async def get_all_users(self, uow: AbstractUnitOfWork,) -> AllUsers:
        async with uow:
            all_users = await uow.users.get_all()
            return AllUsers(users=[User.model_validate(user) for user in all_users])

    async def update_user_by_id(self, uow: AbstractUnitOfWork, user_id: UUID, user: UserUpdate) -> User:
        async with uow:
            updated_user = await uow.users.update_by_id(user_id, user.model_dump(exclude_none=True))
            await uow.commit()
            return User.model_validate(updated_user)

    async def delete_user(self, uow: AbstractUnitOfWork, user_id: UUID) -> None:
        async with uow:
            delete_result = await uow.users.delete_one_by_id(user_id)
            if not delete_result:
                logger.warning(f'User with id {user_id} not found in database')
                raise UserNotFoundException(user_id)
            await uow.commit()


async def get_users_service() -> UsersService:
    return UsersService()
