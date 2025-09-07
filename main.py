import asyncio
import logging
import sys
from config import CONFIG
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.start import router as StartRouter

dp = Dispatcher()

async def main() -> None:
    bot = Bot(token=CONFIG.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(StartRouter)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())