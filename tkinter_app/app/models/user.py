import sqlite3
from app.utils.db import get_connection

class UserModel:
    """Handles database operations for users table."""

    @staticmethod
    def create_user(username: str, password_hash: str, role: str) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "INSERT INTO users (username, password_hash, role) VALUES (?, ?, ?)"
            cursor.execute(query, (username, password_hash, role))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_by_username(username: str) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all_users() -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = "SELECT id, username, role, created_at FROM users"
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def delete_user(user_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM users WHERE id = ?"
            cursor.execute(query, (user_id,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()
