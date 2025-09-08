from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Any, Dict, Awaitable, Callable
from sqlalchemy.ext.asyncio import AsyncSession
from database.ini import session_factory
from database.models.user import User

class UserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        if "user" in data:
            return await handler(event, data)
        
        try:
            tg_id = event.from_user.id
        except AttributeError:
            return await handler(event, data)

        async with session_factory() as session:
            session: AsyncSession
            user = await session.get(User, tg_id)
            if not user:
                user = User(
                    tg_id=tg_id,
                    balance=0.0,
                    mention=event.from_user.mention,
                )
                session.add(user)
                await session.commit()
            
            data["user"] = user

        return await handler(event, data)