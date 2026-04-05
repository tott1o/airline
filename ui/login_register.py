"""
Login and Registration screens.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTabWidget, QMessageBox, QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

from services.user_service import UserService


class LoginRegisterWidget(QWidget):
    """Combined Login / Register widget with tabs."""

    # Signal emitted after successful login: (user_dict)
    login_success = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    # ------------------------------------------------------------------ UI
    def _build_ui(self):
        outer = QVBoxLayout(self)
        outer.setAlignment(Qt.AlignCenter)

        # Card container
        card = QFrame()
        card.setObjectName("authCard")
        card.setFixedWidth(420)
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(30, 30, 30, 30)
        card_layout.setSpacing(15)

        # Title
        title = QLabel("✈  Airline Reservation System")
        title.setObjectName("authTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)

        # Tab widget for Login / Register
        self.tabs = QTabWidget()
        self.tabs.setObjectName("authTabs")
        self.tabs.addTab(self._login_tab(), "Login")
        self.tabs.addTab(self._register_tab(), "Register")
        card_layout.addWidget(self.tabs)

        outer.addWidget(card)

    def _login_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)

        self.login_email = QLineEdit()
        self.login_email.setPlaceholderText("Email address")
        self.login_password = QLineEdit()
        self.login_password.setPlaceholderText("Password")
        self.login_password.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Sign In")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._handle_login)

        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.login_email)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.login_password)
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(btn)
        return w

    def _register_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)
        layout.setSpacing(12)

        self.reg_name = QLineEdit()
        self.reg_name.setPlaceholderText("Full name")
        self.reg_email = QLineEdit()
        self.reg_email.setPlaceholderText("Email address")
        self.reg_phone = QLineEdit()
        self.reg_phone.setPlaceholderText("Phone number")
        self.reg_password = QLineEdit()
        self.reg_password.setPlaceholderText("Password")
        self.reg_password.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Create Account")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self._handle_register)

        layout.addWidget(QLabel("Full Name"))
        layout.addWidget(self.reg_name)
        layout.addWidget(QLabel("Email"))
        layout.addWidget(self.reg_email)
        layout.addWidget(QLabel("Phone"))
        layout.addWidget(self.reg_phone)
        layout.addWidget(QLabel("Password"))
        layout.addWidget(self.reg_password)
        layout.addSpacerItem(QSpacerItem(0, 10, QSizePolicy.Minimum, QSizePolicy.Fixed))
        layout.addWidget(btn)
        return w

    # --------------------------------------------------------------- Handlers
    def _handle_login(self):
        email = self.login_email.text().strip()
        password = self.login_password.text().strip()
        if not email or not password:
            QMessageBox.warning(self, "Validation", "Please fill in all fields.")
            return
        try:
            user = UserService.login(email, password)
            self.login_success.emit(user)
        except ValueError as e:
            QMessageBox.warning(self, "Login Failed", str(e))

    def _handle_register(self):
        name = self.reg_name.text().strip()
        email = self.reg_email.text().strip()
        phone = self.reg_phone.text().strip()
        password = self.reg_password.text().strip()
        if not all([name, email, phone, password]):
            QMessageBox.warning(self, "Validation", "Please fill in all fields.")
            return
        try:
            UserService.register(name, email, password, phone)
            QMessageBox.information(self, "Success", "Account created! You can now log in.")
            self.tabs.setCurrentIndex(0)
            self.login_email.setText(email)
        except ValueError as e:
            QMessageBox.warning(self, "Registration Failed", str(e))
