import sqlite3
from config import DB_NAME
from db import queries

def register_user(telegram_id: int, username: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.REGISTER_USER, (telegram_id, username))
    conn.commit()
    conn.close()
