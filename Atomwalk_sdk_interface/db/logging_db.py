import sqlite3
from datetime import datetime

def init_log_db():
    conn = sqlite3.connect("atomwalk_logs.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            username TEXT,
            device_id TEXT,
            test_result TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_log(username, device_id, result):
    conn = sqlite3.connect("atomwalk_logs.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (timestamp, username, device_id, test_result) VALUES (?, ?, ?, ?)",
                   (datetime.now().isoformat(), username, device_id, result))
    conn.commit()
    conn.close()

def get_all_logs():
    conn = sqlite3.connect("atomwalk_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM logs ORDER BY timestamp DESC")
    rows = cursor.fetchall()
    conn.close()
    return rows
