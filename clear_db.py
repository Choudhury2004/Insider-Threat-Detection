import sqlite3

DB_NAME = "insider_threat.db"

def clear_all_data():
    """Deletes all records from users and activity_logs tables."""
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        print("Clearing 'activity_logs' table...")
        cursor.execute("DELETE FROM activity_logs")
        
        print("Clearing 'users' table...")
        cursor.execute("DELETE FROM users")
        
        # Optional: Reset the auto-increment counters for a true fresh start
        cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('activity_logs', 'users')")

        conn.commit()
        print("Database has been cleared successfully.")
        
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    clear_all_data()