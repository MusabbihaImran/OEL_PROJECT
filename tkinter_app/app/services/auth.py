import hashlib
from app.models.user import UserModel
from app.utils.validators import Validators

class AuthService:
    """Handles authentication and user management logic."""
    
    current_user = None

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """Returns sha256 hex digest of the password."""
        return hashlib.sha256(plain_password.encode()).hexdigest()

    @staticmethod
    def verify_password(plain_password: str, stored_hash: str) -> bool:
        """Verifies a plain text password against a stored hash."""
        return AuthService.hash_password(plain_password) == stored_hash

    @classmethod
    def login(cls, username: str, password: str) -> dict | None:
        """Attempts to log in. Returns user dict on success, None on failure."""
        if not username or not password:
            return None
            
        user = UserModel.get_by_username(username)
        if user and cls.verify_password(password, user['password_hash']):
            cls.current_user = user
            return user
        return None

    @staticmethod
    def register_user(username: str, password: str, role: str = 'staff') -> tuple[bool, str]:
        """Validates input and creates a new user."""
        if not username or len(username) < 3:
            return False, "Username must be at least 3 characters."
            
        is_valid_pwd, pwd_err = Validators.validate_password(password)
        if not is_valid_pwd:
            return False, pwd_err
            
        existing = UserModel.get_by_username(username)
        if existing:
            return False, "Username already exists."
            
        pwd_hash = AuthService.hash_password(password)
        success = UserModel.create_user(username, pwd_hash, role)
        
        if success:
            return True, "User registered successfully."
        else:
            return False, "Database error during registration."

    @classmethod
    def logout(cls):
        """Clears current user session."""
        cls.current_user = None
