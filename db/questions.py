from db.database import get_db
from db.queries import INSERT_QUESTION, SELECT_ALL_QUESTIONS, DELETE_QUESTION

def add_question(text: str, answer: str):
    with get_db() as conn:
        conn.execute(INSERT_QUESTION, (text, answer))
        conn.commit()

def get_all_questions():
    with get_db() as conn:
        cursor = conn.cursor()
        cursor.execute(SELECT_ALL_QUESTIONS)
        return cursor.fetchall()  # Возвращает список кортежей [(id, text, answer), ...]

def delete_question(question_id: int):
    with get_db() as conn:
        conn.execute(DELETE_QUESTION, (question_id,))
        conn.commit()
