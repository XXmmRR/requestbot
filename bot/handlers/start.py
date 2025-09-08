from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from localization.localization import get_translation as _
from loguru import logger

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message):
    logger.info("Start handler called")

    welcome_message = _("start")

    logger.info(f"Welcome message: '{welcome_message}'")

    await message.answer(welcome_message)
