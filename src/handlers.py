from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import (
    Message, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    CallbackQuery
)
from db import users

router = Router()

lang_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Python 🐍", callback_data="lang_python"), 
            InlineKeyboardButton(text="JS 🌐", callback_data="lang_js"), 
            InlineKeyboardButton(text="C# 🎯", callback_data="lang_csharp")
        ]
    ]
)

start_learning_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать обучение 🚀", callback_data="start_learning")]
    ]
)

@router.message(Command("start"))
async def cmd_start(message: Message):
    users.register_user(message.from_user.id, message.from_user.username)
    user_display = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    await message.answer(
        f"Привет, {user_display}! Выберите язык программирования, который хотите изучить:",
        reply_markup=lang_inline_keyboard
    )

@router.callback_query(F.data == "lang_python")
async def info_python(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🐍 *Python* — популярный язык для бэкенда, анализа данных и искусственного интеллекта.", 
        parse_mode="Markdown",
        reply_markup=start_learning_keyboard
    )

@router.callback_query(F.data == "lang_js")
async def info_js(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🌐 *JavaScript (JS)* — главный язык веб-разработки. На нем пишется весь фронтенд.", 
        parse_mode="Markdown",
        reply_markup=start_learning_keyboard
    )

@router.callback_query(F.data == "lang_csharp")
async def info_csharp(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "🎯 *C#* — мощный язык от Microsoft. Используется для создания программ и игр на Unity.", 
        parse_mode="Markdown",
        reply_markup=start_learning_keyboard
    )

help_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Документация Python", url="https://docs.python.org/3/")],
        [InlineKeyboardButton(text="Документация JS", url="https://developer.mozilla.org/ru/docs/Web/JavaScript")],
        [InlineKeyboardButton(text="Документация C#", url="https://learn.microsoft.com/ru-ru/dotnet/csharp/")],
        [InlineKeyboardButton(text="Начать обучение 🚀", callback_data="start_learning")]
    ]
)

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("📚 Полезные ресурсы и ссылки для обучения:", reply_markup=help_inline_keyboard)

@router.message(Command("about"))
async def cmd_about(message: Message):
    about_text = (
        "🤖 *О боте:*\n\n"
        "Привет! Я — твой первый Telegram-бот, созданный для учебы и тестирования функций."
    )
    await message.answer(about_text, parse_mode="Markdown")

@router.callback_query(F.data == "start_learning")
async def process_start_learning(callback: CallbackQuery):
    await callback.answer(text="Начинаем обучение! 🚀 Удачи!", show_alert=True)
