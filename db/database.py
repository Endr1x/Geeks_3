import sqlite3
from config import DB_NAME
from db import queries

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.CREATE_USERS_TABLE)
    cursor.execute(queries.CREATE_TASKS_TABLE)
    conn.commit()
    conn.close()
