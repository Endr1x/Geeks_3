import sqlite3
from config import DATABASE

def get_db():
    conn = sqlite3.connect(DATABASE)
    return conn
