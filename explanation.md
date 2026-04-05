# Code Explanation: Airlines Reservation System

This document provides a detailed breakdown of the project's codebase, organized by its architectural layers.

## 1. Database Layer
The foundation of the project resides in the `db/` directory and the root `database.sql` file.

- **`database.sql`**: Contains the DDL (Data Definition Language) for 8 tables. It also includes "Seed Data" to provide a default admin account and sample flights for testing.
- **`db/connection.py`**: A utility script that uses `mysql.connector` to establish a connection to the MySQL server. It reads credentials from `config.py`.
- **`db/queries.py`**: Provides three core helper functions:
    - `execute_query()`: For `INSERT`, `UPDATE`, `DELETE` (returns last inserted ID).
    - `fetch_all()`: Returns all rows of a query as a list of dictionaries.
    - `fetch_one()`: Returns a single row as a dictionary.
    - *Why this exists:* It abstracts away the complexity of opening/closing cursors and handling database errors in every single file.

## 2. DAO (Data Access Object) Layer
Located in the `dao/` folder, this layer acts as an intermediary between the database and the rest of the application.

- **`user_dao.py`**: Handles user-related queries like registration and login validation.
- **`flight_dao.py`**: Manages data for Flights, Airlines, and Airports. Includes complex `JOIN` queries to fetch human-readable city names instead of ID numbers.
- **`booking_dao.py`**: Handles the creation of booking records, passenger entries, and links them via the `BOOKING_PASSENGER` bridge table.
- **`payment_dao.py`**: Records payment transactions associated with specific bookings.

## 3. Service Layer
Located in the `services/` folder, this is where the "Business Logic" lives. These files coordinate multiple DAOs to perform high-level tasks.

- **`booking_service.py`**: 
    - **Seat Generation**: Uses `random` and `string` to generate seat numbers (e.g., "15D").
    - **Booking Logic**: Performs a sequence of actions: Checks seat availability → Creates a booking record → Inserts each passenger → Updates the `available_seats` count in the `FLIGHT` table.
    - **Cancellation Logic**: Reverses the process by marking the booking as 'Cancelled' and restoring the seat count to the flight.
- **`user_service.py`**: Handles password comparison and session role management (distinguishing between 'admin' and 'customer').

## 4. UI Layer (PyQt5)
The interface is built using **PyQt5**, a powerful cross-platform GUI framework.

- **`main.py`**: 
    - The entry point of the application.
    - **Catppuccin Theme**: It defines a comprehensive CSS-like stylesheet (`STYLESHEET` variable) to give the app a modern, high-tech dark look.
    - Initializes the `QApplication` and the `MainWindow`.
- **`ui/main_window.py`**: Uses a `QStackedWidget` to manage "Screens." It acts as the container that swaps between the Login Panel, Admin Panel, and Customer Panel.
- **`ui/login_register.py`**: A tabbed interface for user authentication.
- **`ui/admin_panel.py`**: A complex dashboard with multiple tabs for managing the airline's infrastructure. It uses `QTableWidget` to display and edit data dynamically.
- **`ui/customer_panel.py`**: Provides a step-by-step workflow for searching flights and booking them via custom pop-up dialogs.

## 5. Summary of Data Flow
1. **User Action:** User clicks "Book" in the UI (`ui/customer_panel.py`).
2. **Service Call:** The UI calls `BookingService.book_flight()`.
3. **Logic execution:** The Service checks seats via `FlightDAO`.
4. **Database Update:** The Service coordinates multiple SQL calls via `BookingDAO` and `FlightDAO`.
5. **UI Refresh:** The UI receives a confirmation and updates the table to show the new booking.
