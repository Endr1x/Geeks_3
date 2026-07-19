import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from db.database import init_db
from src import handlers

async def main():
    logging.basicConfig(level=logging.INFO)
    init_db()
    
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.router)
    
    print("Бот успешно запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен.")
