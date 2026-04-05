# Airlines Reservation System — Walkthrough

## Architecture

```
UI (PyQt5) → Service Layer → DAO Layer → DB Helpers → MySQL
```

## Files Created (18 total)

| Layer | File | Purpose |
|-------|------|---------|
| **Schema** | [database.sql](file:///c:/Users/Adithyan%20unni/Documents/airline/database.sql) | 8 tables + seed data |
| **Config** | [config.py](file:///c:/Users/Adithyan%20unni/Documents/airline/config.py) | MySQL credentials |
| **DB** | [db/connection.py](file:///c:/Users/Adithyan%20unni/Documents/airline/db/connection.py) | [get_connection()](file:///c:/Users/Adithyan%20unni/Documents/airline/db/connection.py#10-13) wrapper |
| **DB** | [db/queries.py](file:///c:/Users/Adithyan%20unni/Documents/airline/db/queries.py) | [execute_query](file:///c:/Users/Adithyan%20unni/Documents/airline/db/queries.py#9-20), [fetch_all](file:///c:/Users/Adithyan%20unni/Documents/airline/db/queries.py#22-32), [fetch_one](file:///c:/Users/Adithyan%20unni/Documents/airline/db/queries.py#34-44) |
| **DAO** | [dao/user_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/user_dao.py) | USERS table SQL |
| **DAO** | [dao/flight_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/flight_dao.py) | FLIGHT/AIRLINE/AIRPORT SQL |
| **DAO** | [dao/booking_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/booking_dao.py) | BOOKING/PASSENGER SQL |
| **DAO** | [dao/payment_dao.py](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/payment_dao.py) | PAYMENT table SQL |
| **Service** | [services/user_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/user_service.py) | Register + login logic |
| **Service** | [services/flight_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/flight_service.py) | Flight/airline/airport CRUD |
| **Service** | [services/booking_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/booking_service.py) | Book/cancel + seat management |
| **Service** | [services/payment_service.py](file:///c:/Users/Adithyan%20unni/Documents/airline/services/payment_service.py) | Payment recording |
| **UI** | [ui/login_register.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/login_register.py) | Login & Register tabs |
| **UI** | [ui/admin_panel.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/admin_panel.py) | Admin dashboard (4 tabs) |
| **UI** | [ui/customer_panel.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/customer_panel.py) | Customer: search, book, cancel |
| **UI** | [ui/main_window.py](file:///c:/Users/Adithyan%20unni/Documents/airline/ui/main_window.py) | Stacked navigation |
| **Entry** | [main.py](file:///c:/Users/Adithyan%20unni/Documents/airline/main.py) | App entry + dark stylesheet |
| **Deps** | [requirements.txt](file:///c:/Users/Adithyan%20unni/Documents/airline/requirements.txt) | PyQt5, mysql-connector-python |

## Setup Instructions

### 1. Set up the database
```sql
-- Open MySQL shell and run:
source C:/Users/Adithyan unni/Documents/airline/database.sql;
```

### 2. Configure credentials
Edit [config.py](file:///c:/Users/Adithyan%20unni/Documents/airline/config.py) — set your MySQL `password`.

### 3. Install dependencies
```bash
cd "C:\Users\Adithyan unni\Documents\airline"
pip install -r requirements.txt
```

### 4. Launch
```bash
python main.py
```

## Usage

| Action | How |
|--------|-----|
| **Admin login** | Email: `admin@airline.com`, Password: `admin123` |
| **Register** | Switch to Register tab, fill form, then login |
| **Search flights** | Customer → Search Flights → select cities → Search |
| **Book** | Select flight → Book → add passengers → pay → Confirm |
| **Cancel** | Customer → My Bookings → select row → Cancel |
| **Admin CRUD** | Admin panel tabs: Flights, Airlines, Airports, Bookings |

## Key Design Decisions

- **DAO pattern** keeps all SQL isolated from business logic — easy to maintain
- **Random seat assignment** (`1A`–`30F`) on booking
- **Seat restoration** on cancellation — [available_seats](file:///c:/Users/Adithyan%20unni/Documents/airline/dao/flight_dao.py#76-81) incremented back
- **Dark Catppuccin theme** applied globally for a modern look
