import unittest
from decimal import Decimal
from app.services.billing_service import BillingService

class TestBillingService(unittest.TestCase):

    def test_calculate_total_basic(self):
        # 2 nights * 5000 + 500 extras = 10500
        price = "5000"
        ci = "2023-10-01"
        co = "2023-10-03"
        extras = "500"
        
        total = BillingService.calculate_total(price, ci, co, extras)
        self.assertEqual(total, Decimal("10500"))

    def test_calculate_total_zero_extras(self):
        # 1 night * 8000 + 0 extras = 8000
        price = "8000"
        ci = "2023-10-01"
        co = "2023-10-02"
        extras = ""
        
        total = BillingService.calculate_total(price, ci, co, extras)
        self.assertEqual(total, Decimal("8000"))

    def test_calculate_total_same_day_raises_error(self):
        price = "5000"
        ci = "2023-10-01"
        co = "2023-10-01"
        extras = "0"
        
        with self.assertRaises(ValueError):
            BillingService.calculate_total(price, ci, co, extras)

if __name__ == '__main__':
    unittest.main()
