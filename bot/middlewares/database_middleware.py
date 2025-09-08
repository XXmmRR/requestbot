from typing import Callable, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import exc


class DbSessionMiddleware(BaseMiddleware):
    """
    Мидлварь, которая предоставляет сессию базы данных в `data` хендлера.

    Сессия автоматически коммитится или откатывается в зависимости от результата выполнения хендлера.
    """

    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            try:
                data["session"] = session
                result = await handler(event, data)

                await session.commit()
                return result
            except exc.SQLAlchemyError:
                await session.rollback()
                raise
            finally:
                await session.close()
