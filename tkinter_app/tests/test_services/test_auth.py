import unittest
from unittest.mock import patch, MagicMock
from app.services.auth import AuthService

class TestAuthService(unittest.TestCase):
    def test_hash_password_returns_hex_string(self):
        pwd = "testPassword123!"
        hashed = AuthService.hash_password(pwd)
        self.assertTrue(isinstance(hashed, str))
        self.assertEqual(len(hashed), 64) # SHA256 length

    def test_verify_password_correct(self):
        pwd = "Password123"
        hashed = AuthService.hash_password(pwd)
        self.assertTrue(AuthService.verify_password(pwd, hashed))

    def test_verify_password_wrong(self):
        pwd = "Password123"
        wrong_pwd = "password123"
        hashed = AuthService.hash_password(pwd)
        self.assertFalse(AuthService.verify_password(wrong_pwd, hashed))

    @patch('app.services.auth.UserModel.get_by_username')
    def test_login_success(self, mock_get_by_username):
        pwd = "Password123"
        mock_user = {'id': 1, 'username': 'testuser', 'password_hash': AuthService.hash_password(pwd)}
        mock_get_by_username.return_value = mock_user

        user = AuthService.login('testuser', pwd)
        self.assertIsNotNone(user)
        self.assertEqual(user['username'], 'testuser')
        self.assertEqual(AuthService.current_user, mock_user)

    @patch('app.services.auth.UserModel.get_by_username')
    def test_login_failure_wrong_password(self, mock_get_by_username):
        mock_user = {'id': 1, 'username': 'testuser', 'password_hash': AuthService.hash_password('Correct123')}
        mock_get_by_username.return_value = mock_user

        user = AuthService.login('testuser', 'Wrong123')
        self.assertIsNone(user)

    @patch('app.services.auth.UserModel.get_by_username')
    def test_login_failure_user_not_found(self, mock_get_by_username):
        mock_get_by_username.return_value = None

        user = AuthService.login('unknown_user', 'Password123')
        self.assertIsNone(user)

if __name__ == '__main__':
    unittest.main()
