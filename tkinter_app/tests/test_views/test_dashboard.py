import unittest
import tkinter as tk
from unittest.mock import patch
from app.views.dashboard import DashboardWindow
from app.services.auth import AuthService

class TestDashboardView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        AuthService.current_user = {'username': 'testadmin', 'role': 'admin'}
        self.app = DashboardWindow(self.root, lambda: None)

    def tearDown(self):
        self.root.destroy()

    @patch('app.views.dashboard.RoomModel.get_all_rooms')
    @patch('app.views.dashboard.BookingModel.get_all_bookings')
    @patch('app.views.dashboard.BillingModel.get_all_bills')
    def test_dashboard_window_opens(self, mock_bills, mock_bookings, mock_rooms):
        mock_rooms.return_value = []
        mock_bookings.return_value = []
        mock_bills.return_value = []
        
        # Calling show_home to verify it doesn't crash and loads UI
        self.app._show_home()
        self.assertIsNotNone(self.app.content_area)

if __name__ == '__main__':
    unittest.main()
