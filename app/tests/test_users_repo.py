from datetime import datetime
from uuid import UUID

from sqlalchemy import text

from app.repositories.users_repository import UsersRepository


# TODO sqlite не поддерживает UUID, поэтому использовать в inmemory его нет смысла для тестирования. Лучше поднять тестовую базу

async def test_add_user(session):
    repo = UsersRepository(session)
    new_user = {
        'email': 'someuser@mail.ru',
        'name': 'Mister',
        'last_name': 'User',
        'birthday': datetime.strptime("2000-01-01", "%Y-%m-%d"),
    }
    created_user = await repo.add(new_user)
    await session.commit()

    all_users = await session.execute(text('SELECT id, email FROM users'))
    row = all_users.fetchone()

    assert created_user.email == 'someuser@mail.ru'
    assert row.email == 'someuser@mail.ru'
    assert UUID(row.id) == created_user.id
