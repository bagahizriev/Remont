import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_application(name: str, phone: str):
    conn = sqlite3.connect('applications.db')
    c = conn.cursor()
    c.execute('INSERT INTO applications (name, phone) VALUES (?, ?)', (name, phone))
    conn.commit()
    conn.close()