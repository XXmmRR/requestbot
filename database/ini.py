
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from config import CONFIG
from collections.abc import AsyncGenerator
from sqlalchemy import exc

class Base(DeclarativeBase):
    pass

connection_string = f"postgresql+asyncpg://{CONFIG.POSTGRES_USER}:{CONFIG.POSTGRES_PASSWORD}@{CONFIG.DB_HOST}:{CONFIG.DB_PORT}/{CONFIG.POSTGRES_DB}"

engine = create_async_engine(
    connection_string,
    echo=True,
)


async def get_db_session_dep() -> AsyncGenerator[AsyncSession, None]:
    "Get async session for Depends"
    factory = async_sessionmaker(engine)
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except exc.SQLAlchemyError:
            await session.rollback()
            raise