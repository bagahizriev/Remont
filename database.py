import sqlite3
from datetime import datetime

DB_FILE = "applications.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            comment TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Новая'
        )
    ''')
    conn.commit()
    conn.close()

def save_application(name: str, phone: str, comment: str | None = None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id FROM applications WHERE phone = ?', (phone,))
    existing = c.fetchone()
    if existing:
        conn.close()
        raise ValueError("Заявка с таким номером телефона уже существует")
    c.execute(
        'INSERT INTO applications (name, phone, comment) VALUES (?, ?, ?)',
        (name, phone, comment)
    )
    conn.commit()
    conn.close()

def get_latest_application_id():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT MAX(id) FROM applications')
    result = c.fetchone()
    conn.close()
    return result[0] if result and result[0] else 0

def get_new_applications(last_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, phone, comment, created_at, status FROM applications WHERE id > ? ORDER BY id ASC', (last_id,))
    apps = c.fetchall()
    conn.close()
    return apps

def get_applications(offset: int = 0, limit: int = 5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, created_at, status FROM applications ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset))
    apps = c.fetchall()
    conn.close()
    return apps

def get_application_detail(app_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, name, phone, comment, created_at, status FROM applications WHERE id = ?', (app_id,))
    app = c.fetchone()
    conn.close()
    return app

def toggle_application_status(app_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT status FROM applications WHERE id = ?', (app_id,))
    current = c.fetchone()
    if not current:
        conn.close()
        return None
    new_status = "Закрыто" if current[0] == "Новая" else "Новая"
    c.execute('UPDATE applications SET status = ? WHERE id = ?', (new_status, app_id))
    conn.commit()
    conn.close()
    return new_status
