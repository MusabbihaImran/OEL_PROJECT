from app.models.feedback_model import FeedbackModel
from app.models.booking import BookingModel
from app.utils.validators import Validators

class FeedbackService:
    """Handles business logic for feedback."""

    @staticmethod
    def submit_feedback(booking_id: str, customer_name: str, rating: str, comment: str) -> tuple[bool, str]:
        try:
            b_id = int(booking_id)
        except ValueError:
            return False, "Booking ID must be a valid number."
            
        # Verify booking exists and is checked out
        booking = BookingModel.get_booking_by_id(b_id)
        if not booking:
            return False, "Booking not found."
        if booking['status'] != 'checked_out':
            return False, "Feedback can only be submitted for checked-out bookings."
            
        v_name, msg_name = Validators.validate_name(customer_name)
        if not v_name: return False, msg_name
        
        v_rating, msg_rating = Validators.validate_rating(rating)
        if not v_rating: return False, msg_rating
        
        success = FeedbackModel.create_feedback(b_id, customer_name, int(rating), comment)
        if success:
            return True, "Feedback submitted successfully."
        return False, "Failed to submit feedback."

    @staticmethod
    def get_all_feedback() -> list[dict]:
        return FeedbackModel.get_all_feedback()

    @staticmethod
    def delete_feedback(feedback_id: int) -> tuple[bool, str]:
        success = FeedbackModel.delete_feedback(feedback_id)
        if success:
            return True, "Feedback deleted successfully."
        return False, "Failed to delete feedback."
