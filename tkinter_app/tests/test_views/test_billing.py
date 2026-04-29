import unittest
import tkinter as tk
from unittest.mock import patch
from app.views.billing import BillingView

class TestBillingView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        
    def tearDown(self):
        self.root.destroy()

    @patch('app.views.billing.BillingService.get_all_bills')
    def test_billing_view_loads(self, mock_get_bills):
        mock_get_bills.return_value = []
        view = BillingView(self.root)
        view.pack()
        
        # Update idletasks to ensure widgets are created
        self.root.update_idletasks()
        
        self.assertIsNotNone(view.tree)
        self.assertIsNotNone(view.right_frame)

if __name__ == '__main__':
    unittest.main()
