"""
User Service — business logic for registration and authentication.
"""

from dao.user_dao import UserDAO


class UserService:

    @staticmethod
    def register(name, email, password, phone):
        """Register a new customer. Returns user_id on success."""
        existing = UserDAO.find_by_email(email)
        if existing:
            raise ValueError("An account with this email already exists.")
        return UserDAO.insert_user(name, email, password, phone, role="customer")

    @staticmethod
    def login(email, password):
        """Authenticate a user. Returns user dict or raises ValueError."""
        user = UserDAO.find_by_email(email)
        if not user:
            raise ValueError("No account found with this email.")
        if user["password"] != password:
            raise ValueError("Incorrect password.")
        return user

    @staticmethod
    def get_all_users():
        return UserDAO.get_all()
