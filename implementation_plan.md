# Airlines Reservation System — Implementation Plan

Student-level Airlines Reservation System with Python, MySQL, and a PyQt5 GUI.

## Proposed Changes

### Project Structure

```
airline/
├── database.sql              # MySQL schema
├── config.py                 # DB connection config
├── db/
│   ├── __init__.py
│   ├── connection.py          # MySQL connector wrapper
│   └── queries.py             # Raw SQL helpers (CRUD)
├── dao/
│   ├── __init__.py
│   ├── user_dao.py            # SQL operations for USERS table
│   ├── flight_dao.py          # SQL operations for FLIGHT, AIRLINE, AIRPORT
│   ├── booking_dao.py         # SQL operations for BOOKING, BOOKING_PASSENGER, PASSENGER
│   └── payment_dao.py         # SQL operations for PAYMENT table
├── services/
│   ├── __init__.py
│   ├── user_service.py        # Register, login, role check
│   ├── flight_service.py      # Search, add, update, delete flights
│   ├── booking_service.py     # Book, cancel, view history
│   └── payment_service.py     # Record & view payments
├── ui/
│   ├── __init__.py
│   ├── main_window.py         # App entry, stacked-widget navigation
│   ├── login_register.py      # Login & registration forms
│   ├── admin_panel.py         # Admin dashboard (flights, airports, airlines, bookings)
│   └── customer_panel.py      # Customer dashboard (search, book, cancel, history)
├── main.py                    # Application entry point
└── requirements.txt           # Dependencies
```

---

### Database Schema  (`database.sql`)

#### [NEW] [database.sql](file:///c:/Users/Adithyan%20unni/Documents/airline/database.sql)

A single `.sql` file that:
1. Creates the database `airline_reservation`
2. Creates all 8 tables with PKs, FKs, and constraints: `USERS`, `AIRLINE`, `AIRPORT`, `FLIGHT`, `PASSENGER`, `BOOKING`, `BOOKING_PASSENGER`, `PAYMENT`
3. Inserts seed data (a default admin, sample airlines, airports, and flights)

---

### Config Module

#### [NEW] [config.py](file:///c:/Users/Adithyan%20unni/Documents/airline/config.py)

Holds MySQL connection settings (`host`, `user`, `password`, `database`) in a dict.

---

### Database Layer (`db/`)

#### [NEW] [connection.py](file:///c:/Users/Adithyan%20unni/Documents/airline/db/connection.py)

- `get_connection()` — returns a `mysql.connector` connection using `config.py`.

#### [NEW] [queries.py](file:///c:/Users/Adithyan%20unni/Documents/airline/db/queries.py)

- Generic `execute_query(sql, params)`, `fetch_all(sql, params)`, `fetch_one(sql, params)` helpers.

---

### DAO Layer (`dao/`)

Each DAO class encapsulates all SQL statements for its table(s), keeping raw SQL out of the service layer.

#### [NEW] [user_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/user_dao.py)

- `insert_user(name, email, password, phone, role)` → returns new `user_id`
- `find_by_email(email)` → returns user row or `None`
- `find_by_id(user_id)` → returns user row
- `get_all()` → list of all users

#### [NEW] [flight_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/flight_dao.py)

- `insert_flight(...)`, `update_flight(...)`, `delete_flight(flight_id)`
- `find_flights(source, destination)` → filtered list
- `get_all_flights()`, `get_flight_by_id(flight_id)`
- `update_available_seats(flight_id, delta)`
- Airline/airport helpers: `insert_airline`, `get_all_airlines`, `insert_airport`, `get_all_airports`, etc.

#### [NEW] [booking_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/booking_dao.py)

- `insert_booking(user_id, flight_id)` → returns `booking_id`
- `insert_passenger(name, age, gender, passport)` → returns `passenger_id`
- `insert_booking_passenger(booking_id, passenger_id, seat_number)`
- `update_booking_status(booking_id, status)`
- `get_bookings_by_user(user_id)`, `get_all_bookings()`
- `get_passengers_for_booking(booking_id)`

#### [NEW] [payment_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/payment_dao.py)

- `insert_payment(booking_id, amount, method)` → returns `payment_id`
- `get_payment_by_booking(booking_id)`

---

### Service Layer (`services/`)

Service classes contain business logic and delegate all database access to DAO classes. Architecture: **UI → Service → DAO → DB**.

#### [NEW] [user_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/user_service.py)

- `register_user(name, email, password, phone)`
- `login(email, password)` → returns user dict with role
- `get_all_users()`

#### [NEW] [flight_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/flight_service.py)

- `search_flights(source, destination, date=None)`
- `get_all_flights()`
- `add_flight(...)`, `update_flight(...)`, `delete_flight(flight_id)`
- Airport/airline CRUD helpers

#### [NEW] [booking_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/booking_service.py)

- `book_flight(user_id, flight_id, passengers)` — creates booking + passenger rows, decrements `available_seats`
- `cancel_booking(booking_id)` — sets status to `Cancelled`, restores seats
- `get_booking_history(user_id)`, `get_all_bookings()`

#### [NEW] [payment_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/payment_service.py)

- `record_payment(booking_id, amount, method)`
- `get_payment_by_booking(booking_id)`

---

### PyQt5 UI Layer (`ui/`)

> [!NOTE]
> Using **PyQt5** — it's the most widely available and student-friendly version.

#### [NEW] [main_window.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/main_window.py)

- `QMainWindow` with a `QStackedWidget` to switch between Login, Admin, and Customer views.
- Professional dark/modern stylesheet applied globally.

#### [NEW] [login_register.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/login_register.py)

- Login form (email + password) with role-based redirect.
- Registration form (name, email, password, phone).
- Tabs or toggle button to switch between Login and Register.

#### [NEW] [admin_panel.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/admin_panel.py)

- Tabbed interface: **Flights** | **Airlines** | **Airports** | **Bookings**
- Each tab has a table view + add/edit/delete buttons with dialog forms.

#### [NEW] [customer_panel.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/customer_panel.py)

- Tabbed interface: **Search Flights** | **My Bookings**
- Search tab: source/destination dropdowns, search button, results table, Book button.
- Booking dialog: collect passenger details (name, age, gender, passport), confirm & pay.
- My Bookings tab: booking history table with Cancel button.

---

### Entry Point

#### [NEW] [main.py](file:///c:/Users/Adithyan%20unni/Documents/airline/main.py)

Creates `QApplication`, applies stylesheet, shows `MainWindow`.

#### [NEW] [requirements.txt](file:///c:/Users/Adithyan%20unni/Documents/airline/requirements.txt)

```
PyQt5
mysql-connector-python
```

---

## Verification Plan

### Manual Verification

1. **Database**: Run `database.sql` in MySQL to create the schema and seed data. Verify tables exist with `SHOW TABLES`.
2. **Launch app**: Run `python main.py`. Confirm the login window appears with a modern dark theme.
3. **Register**: Create a new customer account → confirm success message.
4. **Login as customer**: Search flights, book a ticket with passenger details, view booking in history, cancel booking.
5. **Login as admin** (seeded: `admin@airline.com` / `admin123`): Add/edit/delete flights, airlines, airports. View all bookings.

> [!IMPORTANT]
> Before running, the user must update `config.py` with their local MySQL credentials and run `database.sql` to set up the database.
