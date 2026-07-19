# C-R-U-D

users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER NOT NULL UNIQUE,
        username TEXT
    )
"""

questions_table = """
    CREATE TABLE IF NOT EXISTS questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        question_text TEXT NOT NULL,
        correct_answer TEXT NOT NULL
    )  
"""

results_table = """
    CREATE TABLE IF NOT EXISTS results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id INTEGER,
        score INTEGER
    )
"""

# Запросы для ДЗ-5
INSERT_QUESTION = "INSERT INTO questions (question_text, correct_answer) VALUES (?, ?)"
SELECT_ALL_QUESTIONS = "SELECT id, question_text, correct_answer FROM questions"
DELETE_QUESTION = "DELETE FROM questions WHERE id = ?"
