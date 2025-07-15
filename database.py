import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            start_date TEXT,
            end_date TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_user(user_id, full_name):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    start = datetime.now()
    end = start + timedelta(days=30)
    c.execute("REPLACE INTO users (user_id, full_name, start_date, end_date, status) VALUES (?, ?, ?, ?, ?)",
              (user_id, full_name, start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d'), 'active'))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT start_date, end_date FROM users WHERE user_id = ?", (user_id,))
    user = c.fetchone()
    conn.close()
    return user
