"""
Admin Panel — tabbed interface for managing flights, airlines, airports, bookings.
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, QTableWidget,
    QTableWidgetItem, QPushButton, QHeaderView, QMessageBox,
    QDialog, QFormLayout, QLineEdit, QComboBox, QDateTimeEdit,
    QSpinBox, QLabel
)
from PyQt5.QtCore import Qt, QDateTime, pyqtSignal

from services.flight_service import FlightService
from services.booking_service import BookingService


class AdminPanel(QWidget):
    """Admin dashboard with Flights / Airlines / Airports / Bookings tabs."""

    logout_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Header
        header = QHBoxLayout()
        title = QLabel("Admin Dashboard")
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
        self.tabs.addTab(self._flights_tab(), "Flights")
        self.tabs.addTab(self._airlines_tab(), "Airlines")
        self.tabs.addTab(self._airports_tab(), "Airports")
        self.tabs.addTab(self._bookings_tab(), "Bookings")
        layout.addWidget(self.tabs)

    # =================================================================
    #  FLIGHTS TAB
    # =================================================================
    def _flights_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("+ Add Flight")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self._add_flight)
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self._edit_flight)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("dangerBtn")
        del_btn.clicked.connect(self._delete_flight)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_flights)
        btn_row.addWidget(add_btn)
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        btn_row.addWidget(refresh_btn)
        layout.addLayout(btn_row)

        self.flight_table = QTableWidget()
        self.flight_table.setColumnCount(9)
        self.flight_table.setHorizontalHeaderLabels([
            "ID", "Airline", "Flight #", "From", "To",
            "Departure", "Arrival", "Total", "Available"
        ])
        self.flight_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.flight_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.flight_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.flight_table)
        return w

    def _load_flights(self):
        flights = FlightService.get_all_flights()
        self.flight_table.setRowCount(len(flights))
        for i, f in enumerate(flights):
            self.flight_table.setItem(i, 0, QTableWidgetItem(str(f["flight_id"])))
            self.flight_table.setItem(i, 1, QTableWidgetItem(f["airline_name"]))
            self.flight_table.setItem(i, 2, QTableWidgetItem(f["flight_number"]))
            self.flight_table.setItem(i, 3, QTableWidgetItem(f["source_city"]))
            self.flight_table.setItem(i, 4, QTableWidgetItem(f["destination_city"]))
            self.flight_table.setItem(i, 5, QTableWidgetItem(str(f["departure_time"])))
            self.flight_table.setItem(i, 6, QTableWidgetItem(str(f["arrival_time"])))
            self.flight_table.setItem(i, 7, QTableWidgetItem(str(f["total_seats"])))
            self.flight_table.setItem(i, 8, QTableWidgetItem(str(f["available_seats"])))

    def _add_flight(self):
        dlg = FlightDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            try:
                FlightService.add_flight(**data)
                self._load_flights()
                QMessageBox.information(self, "Success", "Flight added successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _edit_flight(self):
        row = self.flight_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select a flight to edit.")
            return
        flight_id = int(self.flight_table.item(row, 0).text())
        flight = FlightService.get_flight(flight_id)
        dlg = FlightDialog(self, flight)
        if dlg.exec_() == QDialog.Accepted:
            data = dlg.get_data()
            try:
                FlightService.update_flight(flight_id, **data,
                                            available_seats=flight["available_seats"])
                self._load_flights()
                QMessageBox.information(self, "Success", "Flight updated.")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _delete_flight(self):
        row = self.flight_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select a flight to delete.")
            return
        flight_id = int(self.flight_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm",
                                     "Delete this flight? This cannot be undone.",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                FlightService.delete_flight(flight_id)
                self._load_flights()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    # =================================================================
    #  AIRLINES TAB
    # =================================================================
    def _airlines_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("+ Add Airline")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self._add_airline)
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self._edit_airline)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("dangerBtn")
        del_btn.clicked.connect(self._delete_airline)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_airlines)
        btn_row.addWidget(add_btn)
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        btn_row.addWidget(refresh_btn)
        layout.addLayout(btn_row)

        self.airline_table = QTableWidget()
        self.airline_table.setColumnCount(3)
        self.airline_table.setHorizontalHeaderLabels(["ID", "Airline Name", "Code"])
        self.airline_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.airline_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.airline_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.airline_table)
        return w

    def _load_airlines(self):
        airlines = FlightService.get_all_airlines()
        self.airline_table.setRowCount(len(airlines))
        for i, a in enumerate(airlines):
            self.airline_table.setItem(i, 0, QTableWidgetItem(str(a["airline_id"])))
            self.airline_table.setItem(i, 1, QTableWidgetItem(a["airline_name"]))
            self.airline_table.setItem(i, 2, QTableWidgetItem(a["airline_code"]))

    def _add_airline(self):
        dlg = AirlineDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            name, code = dlg.get_data()
            try:
                FlightService.add_airline(name, code)
                self._load_airlines()
                QMessageBox.information(self, "Success", "Airline added.")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _edit_airline(self):
        row = self.airline_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an airline.")
            return
        aid = int(self.airline_table.item(row, 0).text())
        name = self.airline_table.item(row, 1).text()
        code = self.airline_table.item(row, 2).text()
        dlg = AirlineDialog(self, name, code)
        if dlg.exec_() == QDialog.Accepted:
            new_name, new_code = dlg.get_data()
            try:
                FlightService.update_airline(aid, new_name, new_code)
                self._load_airlines()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _delete_airline(self):
        row = self.airline_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an airline.")
            return
        aid = int(self.airline_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm", "Delete this airline?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                FlightService.delete_airline(aid)
                self._load_airlines()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    # =================================================================
    #  AIRPORTS TAB
    # =================================================================
    def _airports_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        btn_row = QHBoxLayout()
        add_btn = QPushButton("+ Add Airport")
        add_btn.setObjectName("primaryBtn")
        add_btn.clicked.connect(self._add_airport)
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self._edit_airport)
        del_btn = QPushButton("Delete")
        del_btn.setObjectName("dangerBtn")
        del_btn.clicked.connect(self._delete_airport)
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_airports)
        btn_row.addWidget(add_btn)
        btn_row.addWidget(edit_btn)
        btn_row.addWidget(del_btn)
        btn_row.addStretch()
        btn_row.addWidget(refresh_btn)
        layout.addLayout(btn_row)

        self.airport_table = QTableWidget()
        self.airport_table.setColumnCount(4)
        self.airport_table.setHorizontalHeaderLabels(["ID", "Airport Name", "City", "Country"])
        self.airport_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.airport_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.airport_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.airport_table)
        return w

    def _load_airports(self):
        airports = FlightService.get_all_airports()
        self.airport_table.setRowCount(len(airports))
        for i, a in enumerate(airports):
            self.airport_table.setItem(i, 0, QTableWidgetItem(str(a["airport_id"])))
            self.airport_table.setItem(i, 1, QTableWidgetItem(a["airport_name"]))
            self.airport_table.setItem(i, 2, QTableWidgetItem(a["city"]))
            self.airport_table.setItem(i, 3, QTableWidgetItem(a["country"]))

    def _add_airport(self):
        dlg = AirportDialog(self)
        if dlg.exec_() == QDialog.Accepted:
            name, city, country = dlg.get_data()
            try:
                FlightService.add_airport(name, city, country)
                self._load_airports()
                QMessageBox.information(self, "Success", "Airport added.")
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _edit_airport(self):
        row = self.airport_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an airport.")
            return
        aid = int(self.airport_table.item(row, 0).text())
        name = self.airport_table.item(row, 1).text()
        city = self.airport_table.item(row, 2).text()
        country = self.airport_table.item(row, 3).text()
        dlg = AirportDialog(self, name, city, country)
        if dlg.exec_() == QDialog.Accepted:
            n, c, co = dlg.get_data()
            try:
                FlightService.update_airport(aid, n, c, co)
                self._load_airports()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    def _delete_airport(self):
        row = self.airport_table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Select", "Please select an airport.")
            return
        aid = int(self.airport_table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm", "Delete this airport?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                FlightService.delete_airport(aid)
                self._load_airports()
            except Exception as e:
                QMessageBox.warning(self, "Error", str(e))

    # =================================================================
    #  BOOKINGS TAB
    # =================================================================
    def _bookings_tab(self):
        w = QWidget()
        layout = QVBoxLayout(w)

        btn_row = QHBoxLayout()
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self._load_bookings)
        btn_row.addStretch()
        btn_row.addWidget(refresh_btn)
        layout.addLayout(btn_row)

        self.booking_table = QTableWidget()
        self.booking_table.setColumnCount(8)
        self.booking_table.setHorizontalHeaderLabels([
            "Booking ID", "Customer", "Flight", "From", "To",
            "Departure", "Date", "Status"
        ])
        self.booking_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.booking_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.booking_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.booking_table)
        return w

    def _load_bookings(self):
        bookings = BookingService.get_all_bookings()
        self.booking_table.setRowCount(len(bookings))
        for i, b in enumerate(bookings):
            self.booking_table.setItem(i, 0, QTableWidgetItem(str(b["booking_id"])))
            self.booking_table.setItem(i, 1, QTableWidgetItem(b["user_name"]))
            self.booking_table.setItem(i, 2, QTableWidgetItem(b["flight_number"]))
            self.booking_table.setItem(i, 3, QTableWidgetItem(b["source_city"]))
            self.booking_table.setItem(i, 4, QTableWidgetItem(b["destination_city"]))
            self.booking_table.setItem(i, 5, QTableWidgetItem(str(b["departure_time"])))
            self.booking_table.setItem(i, 6, QTableWidgetItem(str(b["booking_date"])))
            self.booking_table.setItem(i, 7, QTableWidgetItem(b["booking_status"]))

    # --------------------------------------------------------------- Show
    def showEvent(self, event):
        """Reload data every time the panel is shown."""
        super().showEvent(event)
        self._load_flights()
        self._load_airlines()
        self._load_airports()
        self._load_bookings()


# =====================================================================
#  DIALOGS
# =====================================================================

class FlightDialog(QDialog):
    """Dialog for adding / editing a flight."""

    def __init__(self, parent=None, flight=None):
        super().__init__(parent)
        self.setWindowTitle("Flight Details")
        self.setMinimumWidth(400)
        form = QFormLayout(self)

        # Airline combo
        self.airline_combo = QComboBox()
        self._airlines = FlightService.get_all_airlines()
        for a in self._airlines:
            self.airline_combo.addItem(f"{a['airline_name']} ({a['airline_code']})",
                                       a["airline_id"])

        self.flight_number = QLineEdit()

        # Airport combos
        self.source_combo = QComboBox()
        self.dest_combo = QComboBox()
        self._airports = FlightService.get_all_airports()
        for ap in self._airports:
            label = f"{ap['city']} — {ap['airport_name']}"
            self.source_combo.addItem(label, ap["airport_id"])
            self.dest_combo.addItem(label, ap["airport_id"])

        self.departure = QDateTimeEdit(QDateTime.currentDateTime())
        self.departure.setCalendarPopup(True)
        self.arrival = QDateTimeEdit(QDateTime.currentDateTime().addSecs(7200))
        self.arrival.setCalendarPopup(True)

        self.total_seats = QSpinBox()
        self.total_seats.setRange(1, 500)
        self.total_seats.setValue(180)

        form.addRow("Airline:", self.airline_combo)
        form.addRow("Flight Number:", self.flight_number)
        form.addRow("Source:", self.source_combo)
        form.addRow("Destination:", self.dest_combo)
        form.addRow("Departure:", self.departure)
        form.addRow("Arrival:", self.arrival)
        form.addRow("Total Seats:", self.total_seats)

        btn = QPushButton("Save")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.accept)
        form.addRow(btn)

        # Pre-fill if editing
        if flight:
            idx = self.airline_combo.findData(flight["airline_id"])
            if idx >= 0:
                self.airline_combo.setCurrentIndex(idx)
            self.flight_number.setText(flight["flight_number"])
            src_idx = self.source_combo.findData(flight["source_airport"])
            if src_idx >= 0:
                self.source_combo.setCurrentIndex(src_idx)
            dst_idx = self.dest_combo.findData(flight["destination_airport"])
            if dst_idx >= 0:
                self.dest_combo.setCurrentIndex(dst_idx)
            self.departure.setDateTime(QDateTime(flight["departure_time"]))
            self.arrival.setDateTime(QDateTime(flight["arrival_time"]))
            self.total_seats.setValue(flight["total_seats"])

    def get_data(self):
        return {
            "airline_id": self.airline_combo.currentData(),
            "flight_number": self.flight_number.text().strip(),
            "source_airport": self.source_combo.currentData(),
            "destination_airport": self.dest_combo.currentData(),
            "departure_time": self.departure.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
            "arrival_time": self.arrival.dateTime().toString("yyyy-MM-dd hh:mm:ss"),
            "total_seats": self.total_seats.value(),
        }


class AirlineDialog(QDialog):
    def __init__(self, parent=None, name="", code=""):
        super().__init__(parent)
        self.setWindowTitle("Airline Details")
        form = QFormLayout(self)
        self.name_input = QLineEdit(name)
        self.code_input = QLineEdit(code)
        form.addRow("Airline Name:", self.name_input)
        form.addRow("Airline Code:", self.code_input)
        btn = QPushButton("Save")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.accept)
        form.addRow(btn)

    def get_data(self):
        return self.name_input.text().strip(), self.code_input.text().strip()


class AirportDialog(QDialog):
    def __init__(self, parent=None, name="", city="", country=""):
        super().__init__(parent)
        self.setWindowTitle("Airport Details")
        form = QFormLayout(self)
        self.name_input = QLineEdit(name)
        self.city_input = QLineEdit(city)
        self.country_input = QLineEdit(country)
        form.addRow("Airport Name:", self.name_input)
        form.addRow("City:", self.city_input)
        form.addRow("Country:", self.country_input)
        btn = QPushButton("Save")
        btn.setObjectName("primaryBtn")
        btn.clicked.connect(self.accept)
        form.addRow(btn)

    def get_data(self):
        return (self.name_input.text().strip(),
                self.city_input.text().strip(),
                self.country_input.text().strip())
