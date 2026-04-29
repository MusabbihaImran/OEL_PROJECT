import sqlite3
from app.utils.db import get_connection

class FeedbackModel:
    """Handles database operations for feedback table."""

    @staticmethod
    def create_feedback(booking_id: int, customer_name: str, rating: int, comment: str) -> int | None:
        """Returns inserted feedback ID on success, None on failure."""
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO feedback (booking_id, customer_name, rating, comment) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (booking_id, customer_name, rating, comment))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all_feedback() -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM feedback"
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_feedback_by_booking(booking_id: int) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM feedback WHERE booking_id = ?"
            cursor.execute(query, (booking_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def delete_feedback(feedback_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM feedback WHERE id = ?"
            cursor.execute(query, (feedback_id,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()
