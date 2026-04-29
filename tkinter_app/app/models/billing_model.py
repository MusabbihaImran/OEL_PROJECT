import sqlite3
from app.utils.db import get_connection

class BillingModel:
    """Handles database operations for billing table."""

    @staticmethod
    def create_bill(booking_id: int, room_charges: float, extra_charges: float, extra_description: str, total_amount: float) -> int | None:
        """Returns inserted billing ID on success, None on failure."""
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = """
                INSERT INTO billing (booking_id, room_charges, extra_charges, extra_description, total_amount) 
                VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (booking_id, room_charges, extra_charges, extra_description, total_amount))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_bill_by_booking(booking_id: int) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = """
                SELECT bl.*, 
                       b.check_in_date, b.check_out_date,
                       c.full_name as customer_name,
                       r.room_number, r.price_per_night
                FROM billing bl
                JOIN bookings b ON bl.booking_id = b.id
                JOIN customers c ON b.customer_id = c.id
                JOIN rooms r ON b.room_id = r.id
                WHERE bl.booking_id = ?
            """
            cursor.execute(query, (booking_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all_bills() -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = """
                SELECT bl.id as bill_id, bl.booking_id, bl.room_charges, bl.extra_charges, 
                       bl.total_amount, bl.payment_status, bl.payment_method,
                       c.full_name as customer_name,
                       r.room_number
                FROM billing bl
                JOIN bookings b ON bl.booking_id = b.id
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
    def mark_as_paid(billing_id: int, payment_method: str) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = """
                UPDATE billing 
                SET payment_status = 'paid', payment_method = ?, paid_at = CURRENT_TIMESTAMP 
                WHERE id = ?
            """
            cursor.execute(query, (payment_method, billing_id))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def update_extras(billing_id: int, extra_charges: float, extra_description: str) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            # Also update total amount
            query = """
                UPDATE billing 
                SET extra_charges = ?, extra_description = ?, total_amount = room_charges + ? 
                WHERE id = ?
            """
            cursor.execute(query, (extra_charges, extra_description, extra_charges, billing_id))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()
