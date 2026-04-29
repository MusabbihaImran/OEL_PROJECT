import unittest
from unittest.mock import patch, MagicMock
from app.services.booking_service import BookingService

class TestBookingService(unittest.TestCase):

    @patch('app.services.booking_service.Validators.validate_date_range')
    @patch('app.services.booking_service.RoomModel.get_available_rooms')
    @patch('app.services.booking_service.CustomerModel.get_customer_by_cnic')
    @patch('app.services.booking_service.BookingModel.create_booking')
    @patch('app.services.booking_service.RoomModel.get_room_by_id')
    @patch('app.services.booking_service.BillingModel.create_bill')
    def test_create_booking_valid(self, mock_create_bill, mock_get_room, mock_create_booking, 
                                  mock_get_customer, mock_avail_rooms, mock_val_date):
        
        mock_val_date.return_value = (True, "")
        mock_avail_rooms.return_value = [{'id': 1}]
        mock_get_customer.return_value = {'id': 1}
        mock_create_booking.return_value = 100
        mock_get_room.return_value = {'price_per_night': 5000}
        
        c_data = {'cnic': '12345-1234567-1'}
        success, msg = BookingService.create_booking(c_data, 1, "2023-10-01", "2023-10-03")
        
        self.assertTrue(success)
        mock_create_booking.assert_called_once()
        mock_create_bill.assert_called_once()

    @patch('app.services.booking_service.BookingModel.get_booking_by_id')
    @patch('app.services.booking_service.BookingModel.update_booking_status')
    @patch('app.services.booking_service.RoomModel.update_room_status')
    def test_check_in_updates_status(self, mock_upd_room, mock_upd_booking, mock_get_booking):
        mock_get_booking.return_value = {'status': 'confirmed', 'room_id': 1}
        mock_upd_booking.return_value = True
        
        success, msg = BookingService.check_in(1)
        
        self.assertTrue(success)
        mock_upd_booking.assert_called_with(1, 'checked_in')
        mock_upd_room.assert_called_with(1, 'occupied')

    @patch('app.services.booking_service.BookingModel.get_booking_by_id')
    @patch('app.services.booking_service.BookingModel.update_booking_status')
    @patch('app.services.booking_service.RoomModel.update_room_status')
    def test_check_out_updates_status_and_room(self, mock_upd_room, mock_upd_booking, mock_get_booking):
        mock_get_booking.return_value = {'status': 'checked_in', 'room_id': 1}
        mock_upd_booking.return_value = True
        
        success, msg = BookingService.check_out(1)
        
        self.assertTrue(success)
        mock_upd_booking.assert_called_with(1, 'checked_out')
        mock_upd_room.assert_called_with(1, 'available')

    @patch('app.services.booking_service.BookingModel.cancel_booking')
    def test_cancel_booking_updates_status(self, mock_cancel):
        mock_cancel.return_value = True
        success, msg = BookingService.cancel_booking(1)
        self.assertTrue(success)
        mock_cancel.assert_called_with(1)

if __name__ == '__main__':
    unittest.main()
