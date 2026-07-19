from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from db import users

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    users.register_user(message.from_user.id, message.from_user.username)
    user_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    await message.answer(f"Привет, {user_display}! Я твой первый бот")

@router.message(Command("about"))
async def cmd_about(message: Message):
    about_text = (
        "🤖 *О боте:*\n\n"
        "Привет! Я — твой первый Telegram-бот, созданный для учебы и тестирования функций."
    )
    await message.answer(about_text, parse_mode="Markdown")
