from decimal import Decimal
from datetime import datetime
from app.models.billing_model import BillingModel
from app.utils.validators import Validators

class BillingService:
    """Handles business logic for billing."""

    @staticmethod
    def calculate_total(room_price_per_night: str, check_in: str, check_out: str, extra_charges: str) -> Decimal:
        """Calculates total based on nights, price and extras."""
        try:
            ci_date = datetime.strptime(check_in, "%Y-%m-%d").date()
            co_date = datetime.strptime(check_out, "%Y-%m-%d").date()
            nights = (co_date - ci_date).days
            if nights <= 0:
                raise ValueError("Check-out must be after check-in.")
                
            price = Decimal(room_price_per_night)
            extras = Decimal(extra_charges) if extra_charges else Decimal(0)
            
            return (price * nights) + extras
        except ValueError as e:
            raise e

    @staticmethod
    def add_extras(billing_id: int, extra_charges: str, description: str) -> tuple[bool, str]:
        v_price, msg = Validators.validate_price(extra_charges)
        if not v_price: return False, msg
        
        success = BillingModel.update_extras(billing_id, float(extra_charges), description)
        if success:
            return True, "Extras added successfully."
        return False, "Failed to add extras."

    @staticmethod
    def process_payment(billing_id: int, payment_method: str) -> tuple[bool, str]:
        success = BillingModel.mark_as_paid(billing_id, payment_method)
        if success:
            return True, "Payment processed successfully."
        return False, "Payment failed."

    @staticmethod
    def get_bill_details(booking_id: int) -> dict | None:
        return BillingModel.get_bill_by_booking(booking_id)

    @staticmethod
    def get_all_bills() -> list[dict]:
        return BillingModel.get_all_bills()
