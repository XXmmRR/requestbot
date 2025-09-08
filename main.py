import asyncio
import logging
import sys
from config import CONFIG
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from bot.handlers.start import router as StartRouter
from bot.middlewares.album_middleware import CaptionAlbumMiddleware
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio.client import Redis 

redis_client = Redis(host=CONFIG.REDIS_HOST, port=6379, db=0)

dp = Dispatcher(storage=RedisStorage(redis_client))


async def main() -> None:
    bot = Bot(
        token=CONFIG.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp.message.middleware(CaptionAlbumMiddleware())
    dp.include_router(StartRouter)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
