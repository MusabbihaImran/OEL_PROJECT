import re
from datetime import datetime
from tkinter import messagebox

class Validators:
    """Class containing static methods for all input validation."""

    @staticmethod
    def validate_name(value: str) -> tuple[bool, str]:
        if not value or not re.match(r"^[A-Za-z\s]+$", value):
            return False, "Name must be 2-100 characters, letters and spaces only."
        if not (2 <= len(value) <= 100):
            return False, "Name must be 2-100 characters, letters and spaces only."
        return True, ""

    @staticmethod
    def validate_cnic(value: str) -> tuple[bool, str]:
        if not re.match(r"^\d{5}-\d{7}-\d{1}$", value):
            return False, "CNIC must be in format: 12345-1234567-1"
        return True, ""

    @staticmethod
    def validate_phone(value: str) -> tuple[bool, str]:
        if not re.match(r"^03\d{9}$", value):
            return False, "Phone must be 11 digits starting with 03."
        return True, ""

    @staticmethod
    def validate_email(value: str) -> tuple[bool, str]:
        if not value:
            return True, ""  # Optional
        if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", value):
            return False, "Invalid email format."
        return True, ""

    @staticmethod
    def validate_password(value: str) -> tuple[bool, str]:
        if len(value) < 8 or not any(c.isupper() for c in value) or not any(c.isdigit() for c in value):
            return False, "Password must be 8+ characters with at least 1 uppercase and 1 digit."
        return True, ""

    @staticmethod
    def validate_room_number(value: str) -> tuple[bool, str]:
        if not re.match(r"^[A-Za-z0-9]{2,6}$", value):
            return False, "Room number must be 2-6 alphanumeric characters."
        return True, ""

    @staticmethod
    def validate_price(value: str) -> tuple[bool, str]:
        try:
            val = float(value)
            if val <= 0:
                return False, "Price must be a positive number."
        except ValueError:
            return False, "Price must be a valid number."
        return True, ""

    @staticmethod
    def validate_date_range(check_in: str, check_out: str) -> tuple[bool, str]:
        try:
            ci_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            co_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            today = datetime.now().date()
            
            if ci_date < today:
                return False, "Check-in date cannot be in the past."
            if co_date <= ci_date:
                return False, "Check-out must be after check-in."
                
            return True, ""
        except ValueError:
            return False, "Dates must be in YYYY-MM-DD format."

    @staticmethod
    def validate_floor(value: str) -> tuple[bool, str]:
        try:
            val = int(value)
            if not (1 <= val <= 50):
                return False, "Floor must be a number between 1 and 50."
            return True, ""
        except ValueError:
            return False, "Floor must be an integer."

    @staticmethod
    def validate_rating(value: str) -> tuple[bool, str]:
        try:
            val = int(value)
            if not (1 <= val <= 5):
                return False, "Rating must be between 1 and 5."
            return True, ""
        except ValueError:
            return False, "Rating must be an integer."

def show_validation_error(field_name: str, message: str):
    """Helper to display a validation error popup."""
    messagebox.showerror("Validation Error", f"Invalid {field_name}:\n{message}")
