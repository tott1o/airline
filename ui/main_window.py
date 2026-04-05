"""
Main Window — QStackedWidget-based navigation between Login, Admin, and Customer views.
"""

from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt

from ui.login_register import LoginRegisterWidget
from ui.admin_panel import AdminPanel
from ui.customer_panel import CustomerPanel


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("✈  Airline Reservation System")
        self.resize(1100, 700)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # Login / Register screen (always index 0)
        self.login_widget = LoginRegisterWidget()
        self.login_widget.login_success.connect(self._on_login)
        self.stack.addWidget(self.login_widget)

        # Admin and Customer panels will be created on login
        self.admin_panel = None
        self.customer_panel = None

    def _on_login(self, user):
        """Route to admin or customer panel based on user role."""
        if user["role"] == "admin":
            if self.admin_panel is None:
                self.admin_panel = AdminPanel()
                self.admin_panel.logout_requested.connect(self._logout)
                self.stack.addWidget(self.admin_panel)
            self.stack.setCurrentWidget(self.admin_panel)
        else:
            # Remove previous customer panel if any (different user)
            if self.customer_panel is not None:
                self.stack.removeWidget(self.customer_panel)
                self.customer_panel.deleteLater()
            self.customer_panel = CustomerPanel(user)
            self.customer_panel.logout_requested.connect(self._logout)
            self.stack.addWidget(self.customer_panel)
            self.stack.setCurrentWidget(self.customer_panel)

    def _logout(self):
        """Return to the login screen."""
        self.stack.setCurrentWidget(self.login_widget)
