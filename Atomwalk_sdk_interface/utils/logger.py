import sqlite3
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent / "sdk_logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS test_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            device_id TEXT,
            status TEXT,
            test_name TEXT,
            remarks TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_test_result(device_id, status, test_name, remarks=""):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO test_results (timestamp, device_id, status, test_name, remarks)
        VALUES (?, ?, ?, ?, ?)
    """, (now, device_id, status, test_name, remarks))
    conn.commit()
    conn.close()

def fetch_logs_for_device(device_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM test_results WHERE device_id = ? ORDER BY timestamp DESC LIMIT 10
    """, (device_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_logs_for_device_on_date(device_id, date_str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM test_results 
        WHERE device_id = ? AND DATE(timestamp) = ? 
        ORDER BY timestamp DESC
    """, (device_id, date_str))
    rows = cursor.fetchall()
    conn.close()
    return rows

def fetch_all_logs_on_date(date_str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM test_results 
        WHERE DATE(timestamp) = ? 
        ORDER BY timestamp DESC
    """, (date_str,))
    rows = cursor.fetchall()
    conn.close()
    return rows
