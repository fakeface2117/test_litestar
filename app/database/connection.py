from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

engine = create_async_engine(settings.DB_CONNECTION_STRING)

async_session_maker = async_sessionmaker(bind=engine)


async def get_async_session() -> AsyncSession:
    async with async_session_maker() as session:
        yield session
