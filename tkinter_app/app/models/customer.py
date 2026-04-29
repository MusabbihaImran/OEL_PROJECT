import sqlite3
from app.utils.db import get_connection

class CustomerModel:
    """Handles database operations for customers table."""

    @staticmethod
    def create_customer(full_name: str, cnic: str, phone: str, email: str, address: str) -> int | None:
        """Returns inserted ID on success, None on failure."""
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO customers (full_name, cnic, phone, email, address) VALUES (?, ?, ?, ?, ?)"
            cursor.execute(query, (full_name, cnic, phone, email, address))
            conn.commit()
            return cursor.lastrowid
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_all_customers() -> list[dict]:
        conn = get_connection()
        if not conn: return []
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM customers"
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]
        except sqlite3.Error:
            return []
        finally:
            cursor.close()

    @staticmethod
    def get_customer_by_id(customer_id: int) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM customers WHERE id = ?"
            cursor.execute(query, (customer_id,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def get_customer_by_cnic(cnic: str) -> dict | None:
        conn = get_connection()
        if not conn: return None
        try:
            cursor = conn.cursor()
            query = "SELECT * FROM customers WHERE cnic = ?"
            cursor.execute(query, (cnic,))
            result = cursor.fetchone()
            return dict(result) if result else None
        except sqlite3.Error:
            return None
        finally:
            cursor.close()

    @staticmethod
    def update_customer(customer_id: int, **kwargs) -> bool:
        conn = get_connection()
        if not conn or not kwargs: return False
        try:
            cursor = conn.cursor()
            columns = ", ".join(f"{key} = ?" for key in kwargs.keys())
            values = list(kwargs.values())
            values.append(customer_id)
            query = f"UPDATE customers SET {columns} WHERE id = ?"
            cursor.execute(query, tuple(values))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()

    @staticmethod
    def delete_customer(customer_id: int) -> bool:
        conn = get_connection()
        if not conn: return False
        try:
            cursor = conn.cursor()
            query = "DELETE FROM customers WHERE id = ?"
            cursor.execute(query, (customer_id,))
            conn.commit()
            return True
        except sqlite3.Error:
            return False
        finally:
            cursor.close()
