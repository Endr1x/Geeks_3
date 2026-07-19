import sqlite3
from config import DB_NAME
from db import queries

def add_task(user_id: int, title: str):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.ADD_TASK, (user_id, title))
    conn.commit()
    conn.close()

def get_tasks(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.GET_USER_TASKS, (user_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

def check_owner(task_id: int, user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.CHECK_TASK_OWNER, (task_id, user_id))
    result = cursor.fetchone()
    conn.close()
    return result is not None

def mark_done(task_id: int, user_id: int) -> bool:
    if not check_owner(task_id, user_id):
        return False
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.MARK_TASK_DONE, (task_id, user_id))
    conn.commit()
    conn.close()
    return True

def delete_task(task_id: int, user_id: int) -> bool:
    if not check_owner(task_id, user_id):
        return False
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.DELETE_TASK, (task_id, user_id))
    conn.commit()
    conn.close()
    return True

def get_stats(user_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(queries.GET_USER_STATS, (user_id,))
    stats = cursor.fetchone()
    conn.close()
    return stats if stats else (0, 0, 0)
