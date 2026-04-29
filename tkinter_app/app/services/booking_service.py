from datetime import datetime
from app.models.booking import BookingModel
from app.models.customer import CustomerModel
from app.models.room import RoomModel
from app.models.billing_model import BillingModel
from app.utils.validators import Validators

class BookingService:
    """Handles business logic for bookings."""

    @staticmethod
    def create_booking(customer_data: dict, room_id: int, check_in: str, check_out: str) -> tuple[bool, str]:
        """Validates dates, checks availability, creates customer if needed, creates booking, creates billing."""
        # Date Validation
        v_date, msg_date = Validators.validate_date_range(check_in, check_out)
        if not v_date: return False, msg_date
        
        # Room Availability Check
        avail_rooms = RoomModel.get_available_rooms(check_in, check_out)
        if not any(r['id'] == room_id for r in avail_rooms):
            return False, "Selected room is not available for these dates."
            
        # Get or Create Customer
        customer = CustomerModel.get_customer_by_cnic(customer_data['cnic'])
        if customer:
            customer_id = customer['id']
        else:
            customer_id = CustomerModel.create_customer(
                customer_data['full_name'], 
                customer_data['cnic'], 
                customer_data['phone'], 
                customer_data.get('email', ''), 
                customer_data.get('address', '')
            )
            if not customer_id:
                return False, "Failed to create customer record."

        # Create Booking
        booking_id = BookingModel.create_booking(customer_id, room_id, check_in, check_out)
        if not booking_id:
            return False, "Failed to create booking."
            
        # Calculate Initial Billing
        room = RoomModel.get_room_by_id(room_id)
        ci_date = datetime.strptime(check_in, "%Y-%m-%d").date()
        co_date = datetime.strptime(check_out, "%Y-%m-%d").date()
        nights = (co_date - ci_date).days
        if nights <= 0: nights = 1
        
        room_charges = float(room['price_per_night']) * nights
        
        # Create Billing Record
        BillingModel.create_bill(booking_id, room_charges, 0.0, "", room_charges)
        
        return True, "Booking created successfully."

    @staticmethod
    def cancel_booking(booking_id: int) -> tuple[bool, str]:
        """Updates booking status to cancelled. (Room becomes available automatically based on status queries)."""
        success = BookingModel.cancel_booking(booking_id)
        if success:
            return True, "Booking cancelled successfully."
        return False, "Failed to cancel booking."

    @staticmethod
    def check_in(booking_id: int) -> tuple[bool, str]:
        """Updates booking to 'checked_in', room to 'occupied'."""
        booking = BookingModel.get_booking_by_id(booking_id)
        if not booking or booking['status'] != 'confirmed':
            return False, "Can only check in confirmed bookings."
            
        b_success = BookingModel.update_booking_status(booking_id, 'checked_in')
        if b_success:
            RoomModel.update_room_status(booking['room_id'], 'occupied')
            return True, "Checked in successfully."
        return False, "Check in failed."

    @staticmethod
    def check_out(booking_id: int) -> tuple[bool, str]:
        """Updates booking to 'checked_out', room to 'available'."""
        booking = BookingModel.get_booking_by_id(booking_id)
        if not booking or booking['status'] != 'checked_in':
            return False, "Can only check out checked-in bookings."
            
        b_success = BookingModel.update_booking_status(booking_id, 'checked_out')
        if b_success:
            RoomModel.update_room_status(booking['room_id'], 'available')
            return True, "Checked out successfully."
        return False, "Check out failed."

    @staticmethod
    def get_all_bookings() -> list[dict]:
        return BookingModel.get_all_bookings()
