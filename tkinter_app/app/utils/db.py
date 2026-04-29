import os
import sqlite3
from tkinter import messagebox

class DatabaseConnection:
    """Singleton for Database Connection management."""
    _instance = None
    _connection = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance._connect()
        return cls._instance

    def _connect(self):
        """Initializes connection to local SQLite database."""
        try:
            # Connect to hotel.db in the current directory (or tkinter_app root)
            db_path = os.path.join(os.path.dirname(__file__), '..', '..', 'hotel.db')
            db_path = os.path.abspath(db_path)
            self._connection = sqlite3.connect(db_path, check_same_thread=False)
            
            # Enable dictionary-like access to rows
            self._connection.row_factory = sqlite3.Row
            
            # Enable foreign key support in SQLite
            self._connection.execute("PRAGMA foreign_keys = ON;")
        except sqlite3.Error as err:
            messagebox.showerror("Database Connection Error", f"Failed to connect to database:\n{err}")
            self._connection = None

    def get_connection(self):
        """Returns the active SQLite connection."""
        if self._connection is None:
            self._connect()
        return self._connection

def get_connection():
    """Singleton getter function for database connection."""
    return DatabaseConnection().get_connection()
