import sqlite3
import hashlib

DB_NAME = "insider_threat.db"

def hash_password(password):
    """Hashes a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def add_user(username, password, role):
    """Adds a new user with a specific role to the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    password_hash = hash_password(password)
    
    try:
        cursor.execute("INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)", 
                       (username, password_hash, role))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """Verifies credentials and returns the user's role if successful."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    cursor.execute("SELECT password_hash, role FROM users WHERE username = ?", (username,))
    record = cursor.fetchone()
    conn.close()
    
    if record:
        stored_hash, user_role = record
        if stored_hash == hash_password(password):
            return user_role  # Return the role string ('Admin' or 'User')
    return None # Return None if login fails