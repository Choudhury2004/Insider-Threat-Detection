import sqlite3
import pandas as pd
from datetime import datetime

DB_NAME = "insider_threat.db"

def init_db():
    """Initializes the database with users and activity_logs tables."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Add a 'role' column to the users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS activity_logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            Login_Hour INTEGER,
            Files_Accessed INTEGER,
            Emails_Sent INTEGER,
            USB_Devices_Used INTEGER,
            FOREIGN KEY (username) REFERENCES users (username)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully with user roles.")

# ... (the rest of your db_utils.py file remains the same) ...
def log_activity(username, login_hour, files_accessed, emails_sent, usb_devices):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO activity_logs (username, timestamp, Login_Hour, Files_Accessed, Emails_Sent, USB_Devices_Used)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, timestamp, login_hour, files_accessed, emails_sent, usb_devices))
    conn.commit()
    conn.close()

def log_login(username):
    log_activity(username, datetime.now().hour, 0, 0, 0)
    print(f"Logged login for user: {username}")

def get_all_activity_as_df():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM activity_logs", conn)
    conn.close()
    return df

if __name__ == '__main__':
    init_db()