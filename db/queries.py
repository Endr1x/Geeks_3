CREATE_USERS_TABLE = """
CREATE TABLE IF NOT EXISTS users (
    telegram_id INTEGER PRIMARY KEY,
    username TEXT
);
"""

CREATE_TASKS_TABLE = """
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT NOT NULL,
    is_done INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (telegram_id) ON DELETE CASCADE
);
"""

REGISTER_USER = "INSERT OR IGNORE INTO users (telegram_id, username) VALUES (?, ?);"
ADD_TASK = "INSERT INTO tasks (user_id, title) VALUES (?, ?);"

GET_USER_TASKS = """
SELECT t.id, t.title, t.is_done 
FROM tasks t
INNER JOIN users u ON t.user_id = u.telegram_id
WHERE u.telegram_id = ?;
"""

MARK_TASK_DONE = "UPDATE tasks SET is_done = 1 WHERE id = ? AND user_id = ?;"
CHECK_TASK_OWNER = "SELECT id FROM tasks WHERE id = ? AND user_id = ?;"
DELETE_TASK = "DELETE FROM tasks WHERE id = ? AND user_id = ?;"

GET_USER_STATS = """
SELECT 
    COUNT(id) as total,
    SUM(CASE WHEN is_done = 1 THEN 1 ELSE 0 END) as done,
    SUM(CASE WHEN is_done = 0 THEN 1 ELSE 0 END) as not_done
FROM tasks
WHERE user_id = ?
GROUP BY user_id;
"""
