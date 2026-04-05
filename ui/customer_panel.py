"""
Customer Panel — search flights, book tickets, view/cancel bookings.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QComboBox, QLabel,
    QSpinBox, QGroupBox, QScrollArea, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal

from services.flight_service import FlightService
from services.booking_service import BookingService
from services.payment_service import PaymentService


class CustomerPanel(QWidget):
    """Customer dashboard with Search Flights and My Bookings tabs."""

    logout_requested = pyqtSignal()

    def __init__(self, user, parent=None):
        super().__init__(parent)
        self.user = user
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel(f"Welcome, {self.user['name']}")
        title.setObjectName("panelTitle")
        header.addWidget(title)
        header.addStretch()
        logout_btn = QPushButton("Logout")
        logout_btn.setObjectName("logoutBtn")
        logout_btn.clicked.connect(self.logout_requested.emit)
        header.addWidget(logout_btn)
        layout.addLayout(header)

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self._search_tab(), "Search Flights")
        self.tabs.addTab(self._bookings_tab(), "My Bookings")
        layout.addWidget(self.tabs)

    # =================================================================
    #  SEARCH FLIGHTS TAB
    # =================================================================
    def _search_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        # Search bar
        search_row = QHBoxLayout()
        self.source_combo = QComboBox()
        self.dest_combo = QComboBox()
        self._airports = FlightService.get_all_airports()
        for ap in self._airports:
            label = f"{ap['city']}"
            self.source_combo.addItem(label, ap["airport_id"])
            self.dest_combo.addItem(label, ap["airport_id"])

        search_btn = QPushButton("Search")
        search_btn.setObjectName("primaryBtn")
        search_btn.clicked.connect(self._search_flights)

        search_row.addWidget(QLabel("From:"))
        search_row.addWidget(self.source_combo)
        search_row.addWidget(QLabel("To:"))
        search_row.addWidget(self.dest_combo)
        search_row.addWidget(search_btn)
        layout.addLayout(search_row)

        # Results table
        self.search_table = QTableWidget()
        self.search_table.setColumnCount(8)
        self.search_table.setHorizontalHeaderLabels([
            "ID", "Airline", "Flight #", "From", "To",
            "Departure", "Arrival", "Seats"
        ])
        self.search_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.search_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.search_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.search_table)

        # Book button
        book_btn = QPushButton("Book Selected Flight")
        book_btn.setObjectName("primaryBtn")
        book_btn.clicked.connect(self._book_flight)
        layout.addWidget(book_btn)

        return w

    def _search_flights(self):
        src = self.source_combo.currentData()
        dst = self.dest_combo.currentData()
        if src == dst:
            QMessageBox.warning(self, "Validation",
                                "Source and destination must be different.")
            return
        flights = FlightService.search_flights(src, dst)
        self.search_table.setRowCount(len(flights))
        for i, f in enumerate(flights):
            self.search_table.setItem(i, 0, QTableWidgetItem(str(f["flight_id"])))
            self.search_table.setItem(i, 1, QTableWidgetItem(f["airline_name"]))
            self.search_table.setItem(i, 2, QTableWidgetItem(f["flight_number"]))
            self.search_table.setItem(i, 3, QTableWidgetItem(f["source_city"]))
            self.search_table.setItem(i, 4, QTableWidgetItem(f["destination_city"]))
            self.search_table.setItem(i, 5, QTableWidgetItem(str(f["departure_time"])))
            self.search_table.setItem(i, 6, QTableWidgetItem(str(f["arrival_time"])))
            self.search_table.setItem(i, 7, QTableWidgetItem(str(f["available_seats"])))
        if not flights:
            QMessageBox.information(self, "No Results",
                                    "No available flights found for this route.")

    def _book_flight(self):
        row = self.search_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select a flight to book.")
            return
        flight_id = int(self.search_table.item(row, 0).text())
        dlg = BookingDialog(self, flight_id, self.user["user_id"])
        if dlg.exec_() == QDialog.Accepted:
            self._search_flights()   # Refresh to update seat count
            self._load_bookings()
            QMessageBox.information(self, "Success", "Booking confirmed!")

    # =================================================================
    #  MY BOOKINGS TAB
    # =================================================================
    def _bookings_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        btn_row = QHBoxLayout()
        cancel_btn = QPushButton("Cancel Booking")
        cancel_btn.setObjectName("dangerBtn")
        cancel_btn.clicked.connect(self._cancel_booking)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_bookings)
        btn_row.addWidget(cancel_btn)
        btn_row.addStretch()
        btn_row.addWidget(refresh_btn)
        layout.addLayout(btn_row)

        self.bookings_table = QTableWidget()
        self.bookings_table.setColumnCount(7)
        self.bookings_table.setHorizontalHeaderLabels([
            "Booking ID", "Flight", "From", "To",
            "Departure", "Date", "Status"
        ])
        self.bookings_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.bookings_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.bookings_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.bookings_table)
        return w

    def _load_bookings(self):
        bookings = BookingService.get_booking_history(self.user["user_id"])
        self.bookings_table.setRowCount(len(bookings))
        for i, b in enumerate(bookings):
            self.bookings_table.setItem(i, 0, QTableWidgetItem(str(b["booking_id"])))
            self.bookings_table.setItem(i, 1, QTableWidgetItem(b["flight_number"]))
            self.bookings_table.setItem(i, 2, QTableWidgetItem(b["source_city"]))
            self.bookings_table.setItem(i, 3, QTableWidgetItem(b["destination_city"]))
            self.bookings_table.setItem(i, 4, QTableWidgetItem(str(b["departure_time"])))
            self.bookings_table.setItem(i, 5, QTableWidgetItem(str(b["booking_date"])))
            self.bookings_table.setItem(i, 6, QTableWidgetItem(b["booking_status"]))

    def _cancel_booking(self):
        row = self.bookings_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select a booking to cancel.")
            return
        booking_id = int(self.bookings_table.item(row, 0).text())
        status = self.bookings_table.item(row, 6).text()
        if status == "Cancelled":
            QMessageBox.information(self, "Info", "This booking is already cancelled.")
            return
        reply = QMessageBox.question(self, "Confirm",
                                     "Cancel this booking?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                BookingService.cancel_booking(booking_id)
                self._load_bookings()
                QMessageBox.information(self, "Cancelled", "Booking cancelled successfully.")
            except ValueError as e:
                QMessageBox.warning(self, "Error", str(e))

    # --------------------------------------------------------------- Show
    def showEvent(self, event):
        super().showEvent(event)
        self._load_bookings()


# =====================================================================
#  BOOKING DIALOG
# =====================================================================

class BookingDialog(QDialog):
    """Dialog to enter passenger details and complete a booking."""

    def __init__(self, parent, flight_id, user_id):
        super().__init__(parent)
        self.setWindowTitle("Book Flight")
        self.setMinimumWidth(500)
        self.flight_id = flight_id
        self.user_id = user_id

        layout = QVBoxLayout(self)

        # Number of passengers
        top_row = QHBoxLayout()
        top_row.addWidget(QLabel("Number of passengers:"))
        self.num_pax = QSpinBox()
        self.num_pax.setRange(1, 9)
        self.num_pax.setValue(1)
        self.num_pax.valueChanged.connect(self._rebuild_passenger_forms)
        top_row.addWidget(self.num_pax)
        top_row.addStretch()
        layout.addLayout(top_row)

        # Scroll area for passenger forms
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.pax_container = QWidget()
        self.pax_layout = QVBoxLayout(self.pax_container)
        self.scroll.setWidget(self.pax_container)
        layout.addWidget(self.scroll)

        self.pax_forms = []
        self._rebuild_passenger_forms()

        # Payment method
        pay_row = QHBoxLayout()
        pay_row.addWidget(QLabel("Payment Method:"))
        self.pay_method = QComboBox()
        self.pay_method.addItems(["Credit Card", "Debit Card", "UPI", "Net Banking"])
        pay_row.addWidget(self.pay_method)
        self.amount_input = QLineEdit("5000")
        self.amount_input.setPlaceholderText("Amount (₹)")
        pay_row.addWidget(QLabel("Amount (₹):"))
        pay_row.addWidget(self.amount_input)
        layout.addLayout(pay_row)

        # Confirm button
        confirm_btn = QPushButton("Confirm Booking")
        confirm_btn.setObjectName("primaryBtn")
        confirm_btn.clicked.connect(self._confirm)
        layout.addWidget(confirm_btn)

    def _rebuild_passenger_forms(self):
        # Clear existing
        for f in self.pax_forms:
            f["group"].setParent(None)
        self.pax_forms = []

        for i in range(self.num_pax.value()):
            group = QGroupBox(f"Passenger {i + 1}")
            form = QFormLayout(group)
            name = QLineEdit()
            age = QSpinBox()
            age.setRange(1, 120)
            age.setValue(25)
            gender = QComboBox()
            gender.addItems(["Male", "Female", "Other"])
            passport = QLineEdit()
            form.addRow("Name:", name)
            form.addRow("Age:", age)
            form.addRow("Gender:", gender)
            form.addRow("Passport #:", passport)
            self.pax_layout.addWidget(group)
            self.pax_forms.append({
                "group": group, "name": name,
                "age": age, "gender": gender, "passport": passport
            })

    def _confirm(self):
        passengers = []
        for f in self.pax_forms:
            name = f["name"].text().strip()
            if not name:
                QMessageBox.warning(self, "Validation",
                                    "Please fill in all passenger names.")
                return
            passengers.append({
                "name": name,
                "age": f["age"].value(),
                "gender": f["gender"].currentText(),
                "passport_number": f["passport"].text().strip(),
            })

        amount_text = self.amount_input.text().strip()
        try:
            amount = float(amount_text)
        except ValueError:
            QMessageBox.warning(self, "Validation", "Please enter a valid amount.")
            return

        try:
            booking_id = BookingService.book_flight(
                self.user_id, self.flight_id, passengers
            )
            PaymentService.record_payment(
                booking_id, amount, self.pay_method.currentText()
            )
            self.accept()
        except ValueError as e:
            QMessageBox.warning(self, "Booking Failed", str(e))
