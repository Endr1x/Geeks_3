import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import BOT_TOKEN
from src.handlers import router
from db.database import get_db
from db.queries import questions_table

logging.basicConfig(level=logging.INFO)

# Инициализируем БД при старте
def init_db():
    with get_db() as conn:
        conn.execute(questions_table)
        conn.commit()

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
dp.include_router(router)

async def main():
    init_db()  # Создаем таблицы, если их нет
    print("Бот запущен и таблицы БД проверены!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
