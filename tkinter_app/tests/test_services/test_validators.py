import unittest
from datetime import datetime, timedelta
from app.utils.validators import Validators

class TestValidators(unittest.TestCase):

    def test_validate_name_valid(self):
        self.assertTrue(Validators.validate_name("John Doe")[0])

    def test_validate_name_too_short(self):
        self.assertFalse(Validators.validate_name("J")[0])

    def test_validate_name_numbers_rejected(self):
        self.assertFalse(Validators.validate_name("John123")[0])

    def test_validate_cnic_valid(self):
        self.assertTrue(Validators.validate_cnic("12345-1234567-1")[0])

    def test_validate_cnic_wrong_format(self):
        self.assertFalse(Validators.validate_cnic("1234-1234567-1")[0])
        self.assertFalse(Validators.validate_cnic("1234512345671")[0])

    def test_validate_phone_valid(self):
        self.assertTrue(Validators.validate_phone("03001234567")[0])

    def test_validate_phone_too_short(self):
        self.assertFalse(Validators.validate_phone("0300123456")[0])

    def test_validate_phone_wrong_prefix(self):
        self.assertFalse(Validators.validate_phone("04001234567")[0])

    def test_validate_email_valid(self):
        self.assertTrue(Validators.validate_email("test@example.com")[0])

    def test_validate_email_invalid(self):
        self.assertFalse(Validators.validate_email("test@.com")[0])

    def test_validate_email_empty_allowed(self):
        self.assertTrue(Validators.validate_email("")[0])

    def test_validate_password_valid(self):
        self.assertTrue(Validators.validate_password("Password123")[0])

    def test_validate_password_no_uppercase(self):
        self.assertFalse(Validators.validate_password("password123")[0])

    def test_validate_password_too_short(self):
        self.assertFalse(Validators.validate_password("Pass1")[0])

    def test_validate_price_valid(self):
        self.assertTrue(Validators.validate_price("5000.50")[0])

    def test_validate_price_zero_rejected(self):
        self.assertFalse(Validators.validate_price("0")[0])

    def test_validate_price_negative_rejected(self):
        self.assertFalse(Validators.validate_price("-500")[0])

    def test_validate_date_range_valid(self):
        ci = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        co = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        self.assertTrue(Validators.validate_date_range(ci, co)[0])

    def test_validate_date_range_checkout_before_checkin(self):
        ci = (datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
        co = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
        self.assertFalse(Validators.validate_date_range(ci, co)[0])

if __name__ == '__main__':
    unittest.main()
