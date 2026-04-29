import sqlite3
from app.utils.db import get_connection

class BookingModel:
    """Handles database operations for bookings table."""

    @staticmethod
    def create_booking(customer_id: int, room_id: int, check_in_date: str, check_out_date: str) -> int | None:
        """Returns inserted booking ID on success, None on failure."""
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO bookings (customer_id, room_id, check_in_date, check_out_date) 
                VALUES (?, ?, ?, ?)
            """
            cursor.execute(query, (customer_id, room_id, check_in_date, check_out_date))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all_bookings() -> list[dict]:
        """JOIN with customers and rooms to return full info."""
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = """
                SELECT b.id as booking_id, b.check_in_date, b.check_out_date, b.status,
                       c.full_name as customer_name, c.cnic, 
                       r.room_number, r.type, r.price_per_night
                FROM bookings b
                JOIN customers c ON b.customer_id = c.id
                JOIN rooms r ON b.room_id = r.id
            """
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_booking_by_id(booking_id: int) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = """
                SELECT b.id as booking_id, b.check_in_date, b.check_out_date, b.status, b.room_id, b.customer_id,
                       c.full_name as customer_name, c.cnic,
                       r.room_number, r.price_per_night
                FROM bookings b
                JOIN customers c ON b.customer_id = c.id
                JOIN rooms r ON b.room_id = r.id
                WHERE b.id = ?
            """
            cursor.execute(query, (booking_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_bookings_by_customer(customer_id: int) -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM bookings WHERE customer_id = ?"
            cursor.execute(query, (customer_id,))
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def update_booking_status(booking_id: int, status: str) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "UPDATE bookings SET status = ? WHERE id = ?"
            cursor.execute(query, (status, booking_id))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def cancel_booking(booking_id: int) -> bool:
        return BookingModel.update_booking_status(booking_id, 'cancelled')

    @staticmethod
    def delete_booking(booking_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM bookings WHERE id = ?"
            cursor.execute(query, (booking_id,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()
