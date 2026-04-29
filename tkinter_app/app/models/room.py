import sqlite3
from app.utils.db import get_connection

class RoomModel:
    """Handles database operations for rooms table."""

    @staticmethod
    def create_room(room_number: str, type: str, price_per_night: float, floor: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "INSERT INTO rooms (room_number, type, price_per_night, floor) VALUES (?, ?, ?, ?)"
            cursor.execute(query, (room_number, type, price_per_night, floor))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def get_all_rooms() -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM rooms"
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_available_rooms(check_in: str, check_out: str) -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            # Find rooms NOT in bookings that overlap with check_in and check_out
            query = """
                SELECT * FROM rooms 
                WHERE status != 'maintenance' 
                AND id NOT IN (
                    SELECT room_id FROM bookings 
                    WHERE status IN ('confirmed', 'checked_in')
                    AND (check_in_date < ? AND check_out_date > ?)
                )
            """
            cursor.execute(query, (check_out, check_in))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_room_by_id(room_id: int) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM rooms WHERE id = ?"
            cursor.execute(query, (room_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def update_room_status(room_id: int, status: str) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "UPDATE rooms SET status = ? WHERE id = ?"
            cursor.execute(query, (status, room_id))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_room(room_id: int, **kwargs) -> bool:
        conn = get_connection()
        if not conn or not kwargs: return False
        try:
            cursor = conn.cursor()
            columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
            values = list(kwargs.values())
            values.append(room_id)
            query = f"UPDATE rooms SET {columns} WHERE id = ?"
            cursor.execute(query, tuple(values))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete_room(room_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM rooms WHERE id = ?"
            cursor.execute(query, (room_id,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()
