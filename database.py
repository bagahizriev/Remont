import sqlite3
from datetime import datetime

DB_FILE = "applications.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Проверяем, существует ли таблица и есть ли столбец name
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='applications'")
    table_exists = c.fetchone()
    
    if table_exists:
        # Проверяем структуру таблицы
        c.execute("PRAGMA table_info(applications)")
        columns = [column[1] for column in c.fetchall()]
        if 'name' in columns:
            # Миграция: создаем новую таблицу без поля name
            c.execute('''
                CREATE TABLE applications_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    phone TEXT NOT NULL,
                    comment TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'Новая'
                )
            ''')
            c.execute('''
                INSERT INTO applications_new (id, phone, comment, created_at, status)
                SELECT id, phone, comment, created_at, status FROM applications
            ''')
            c.execute('DROP TABLE applications')
            c.execute('ALTER TABLE applications_new RENAME TO applications')
    else:
        # Создаем новую таблицу
        c.execute('''
            CREATE TABLE applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                phone TEXT NOT NULL,
                comment TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'Новая'
            )
        ''')
    conn.commit()
    conn.close()

def save_application(phone: str, comment: str | None = None):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id FROM applications WHERE phone = ?', (phone,))
    existing = c.fetchone()
    if existing:
        conn.close()
        raise ValueError("Заявка с таким номером телефона уже существует")
    c.execute(
        'INSERT INTO applications (phone, comment) VALUES (?, ?)',
        (phone, comment)
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
    c.execute('SELECT id, phone, comment, created_at, status FROM applications WHERE id > ? ORDER BY id ASC', (last_id,))
    apps = c.fetchall()
    conn.close()
    return apps

def get_applications(offset: int = 0, limit: int = 5):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, phone, created_at, status FROM applications ORDER BY id DESC LIMIT ? OFFSET ?', (limit, offset))
    apps = c.fetchall()
    conn.close()
    return apps

def get_application_detail(app_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, phone, comment, created_at, status FROM applications WHERE id = ?', (app_id,))
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
