import os
import sqlite3
from app.utils.db import get_connection

def initialize():
    """Initializes the database using schema.sql if it's empty."""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'hotel.db')
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'schema.sql')
    
    conn = get_connection()
    if not conn:
        return
        
    try:
        # Check if users table exists to determine if we need to initialize
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not cursor.fetchone():
            # Table doesn't exist, execute schema
            if os.path.exists(schema_path):
                with open(schema_path, 'r', encoding='utf-8') as f:
                    schema_script = f.read()
                cursor.executescript(schema_script)
                conn.commit()
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        cursor.close()
