from app.models.room import RoomModel
from app.utils.validators import Validators

class RoomService:
    """Handles business logic for rooms."""

    @staticmethod
    def add_room(room_number: str, room_type: str, price: str, floor: str) -> tuple[bool, str]:
        """Validates all inputs before calling model."""
        v_room, msg_room = Validators.validate_room_number(room_number)
        if not v_room: return False, msg_room
        
        v_price, msg_price = Validators.validate_price(price)
        if not v_price: return False, msg_price
        
        v_floor, msg_floor = Validators.validate_floor(floor)
        if not v_floor: return False, msg_floor
        
        success = RoomModel.create_room(room_number, room_type, float(price), int(floor))
        if success:
            return True, "Room added successfully."
        return False, "Failed to add room or room number already exists."

    @staticmethod
    def get_all_rooms() -> list[dict]:
        return RoomModel.get_all_rooms()

    @staticmethod
    def get_available_rooms(check_in: str, check_out: str) -> list[dict]:
        return RoomModel.get_available_rooms(check_in, check_out)

    @staticmethod
    def update_room_status(room_id: int, status: str) -> bool:
        return RoomModel.update_room_status(room_id, status)

    @staticmethod
    def delete_room(room_id: int) -> tuple[bool, str]:
        """Check if room has active bookings before deleting."""
        # Simplified: We just attempt to delete. If it violates FK constraints, it fails.
        success = RoomModel.delete_room(room_id)
        if success:
            return True, "Room deleted successfully."
        return False, "Cannot delete room. It may be linked to existing bookings."

    @staticmethod
    def edit_room(room_id: int, **kwargs) -> tuple[bool, str]:
        """Edits an existing room with validation on updated fields."""
        if 'room_number' in kwargs:
            v, m = Validators.validate_room_number(kwargs['room_number'])
            if not v: return False, m
        if 'price_per_night' in kwargs:
            v, m = Validators.validate_price(str(kwargs['price_per_night']))
            if not v: return False, m
            kwargs['price_per_night'] = float(kwargs['price_per_night'])
        if 'floor' in kwargs:
            v, m = Validators.validate_floor(str(kwargs['floor']))
            if not v: return False, m
            kwargs['floor'] = int(kwargs['floor'])
            
        success = RoomModel.update_room(room_id, **kwargs)
        if success:
            return True, "Room updated successfully."
        return False, "Failed to update room."
