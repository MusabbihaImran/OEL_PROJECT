import unittest
import tkinter as tk
from app.views.login import LoginWindow

class TestLoginView(unittest.TestCase):

    def setUp(self):
        self.root = tk.Tk()
        self.app = LoginWindow(self.root, lambda: None)

    def tearDown(self):
        self.root.destroy()

    def test_login_window_opens(self):
        # Check if basic widgets exist
        self.assertIsNotNone(self.app.user_entry)
        self.assertIsNotNone(self.app.pwd_entry)
        self.assertIsNotNone(self.app.login_btn)
        self.assertIsNotNone(self.app.error_lbl)

    def test_login_empty_username_shows_error(self):
        self.app.user_entry.insert(0, "")
        self.app.pwd_entry.insert(0, "password")
        self.app.login_btn.invoke()
        self.assertEqual(self.app.error_lbl.cget("text"), "Username must be at least 3 characters.")

    def test_login_empty_password_shows_error(self):
        self.app.user_entry.insert(0, "admin")
        self.app.pwd_entry.insert(0, "")
        self.app.login_btn.invoke()
        self.assertEqual(self.app.error_lbl.cget("text"), "Password cannot be empty.")

if __name__ == '__main__':
    unittest.main()
