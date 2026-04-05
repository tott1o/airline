-- ============================================================
-- Airlines Reservation System - Database Schema
-- ============================================================

CREATE DATABASE IF NOT EXISTS airline_reservation;
USE airline_reservation;

-- -----------------------------------------------------------
-- 1. USERS table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS USERS (
    user_id       INT AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(100)  NOT NULL,
    email         VARCHAR(150)  NOT NULL UNIQUE,
    password      VARCHAR(255)  NOT NULL,
    phone         VARCHAR(20),
    role          ENUM('admin', 'customer') NOT NULL DEFAULT 'customer'
);

-- -----------------------------------------------------------
-- 2. AIRLINE table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS AIRLINE (
    airline_id    INT AUTO_INCREMENT PRIMARY KEY,
    airline_name  VARCHAR(100) NOT NULL,
    airline_code  VARCHAR(10)  NOT NULL UNIQUE
);

-- -----------------------------------------------------------
-- 3. AIRPORT table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS AIRPORT (
    airport_id    INT AUTO_INCREMENT PRIMARY KEY,
    airport_name  VARCHAR(150) NOT NULL,
    city          VARCHAR(100) NOT NULL,
    country       VARCHAR(100) NOT NULL
);

-- -----------------------------------------------------------
-- 4. FLIGHT table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS FLIGHT (
    flight_id            INT AUTO_INCREMENT PRIMARY KEY,
    airline_id           INT NOT NULL,
    flight_number        VARCHAR(20)  NOT NULL,
    source_airport       INT NOT NULL,
    destination_airport  INT NOT NULL,
    departure_time       DATETIME NOT NULL,
    arrival_time         DATETIME NOT NULL,
    total_seats          INT NOT NULL DEFAULT 180,
    available_seats      INT NOT NULL DEFAULT 180,
    FOREIGN KEY (airline_id)          REFERENCES AIRLINE(airline_id) ON DELETE CASCADE,
    FOREIGN KEY (source_airport)      REFERENCES AIRPORT(airport_id) ON DELETE CASCADE,
    FOREIGN KEY (destination_airport) REFERENCES AIRPORT(airport_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- 5. PASSENGER table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS PASSENGER (
    passenger_id    INT AUTO_INCREMENT PRIMARY KEY,
    name            VARCHAR(100) NOT NULL,
    age             INT NOT NULL,
    gender          ENUM('Male', 'Female', 'Other') NOT NULL,
    passport_number VARCHAR(50)
);

-- -----------------------------------------------------------
-- 6. BOOKING table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS BOOKING (
    booking_id      INT AUTO_INCREMENT PRIMARY KEY,
    user_id         INT NOT NULL,
    flight_id       INT NOT NULL,
    booking_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    booking_status  ENUM('Confirmed', 'Cancelled') NOT NULL DEFAULT 'Confirmed',
    FOREIGN KEY (user_id)   REFERENCES USERS(user_id)   ON DELETE CASCADE,
    FOREIGN KEY (flight_id) REFERENCES FLIGHT(flight_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- 7. BOOKING_PASSENGER table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS BOOKING_PASSENGER (
    booking_passenger_id  INT AUTO_INCREMENT PRIMARY KEY,
    booking_id            INT NOT NULL,
    passenger_id          INT NOT NULL,
    seat_number           VARCHAR(10),
    FOREIGN KEY (booking_id)   REFERENCES BOOKING(booking_id)     ON DELETE CASCADE,
    FOREIGN KEY (passenger_id) REFERENCES PASSENGER(passenger_id) ON DELETE CASCADE
);

-- -----------------------------------------------------------
-- 8. PAYMENT table
-- -----------------------------------------------------------
CREATE TABLE IF NOT EXISTS PAYMENT (
    payment_id      INT AUTO_INCREMENT PRIMARY KEY,
    booking_id      INT NOT NULL,
    amount          DECIMAL(10, 2) NOT NULL,
    payment_date    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    payment_method  ENUM('Credit Card', 'Debit Card', 'UPI', 'Net Banking') NOT NULL,
    payment_status  ENUM('Completed', 'Pending', 'Failed') NOT NULL DEFAULT 'Completed',
    FOREIGN KEY (booking_id) REFERENCES BOOKING(booking_id) ON DELETE CASCADE
);


-- ============================================================
-- SEED DATA
-- ============================================================

-- Default admin user (password: admin123)
INSERT INTO USERS (name, email, password, phone, role) VALUES
('Admin', 'admin@airline.com', 'admin123', '9999999999', 'admin');

-- Sample airlines
INSERT INTO AIRLINE (airline_name, airline_code) VALUES
('Air India',        'AI'),
('IndiGo',           '6E'),
('SpiceJet',         'SG'),
('Vistara',          'UK'),
('Go First',         'G8');

-- Sample airports
INSERT INTO AIRPORT (airport_name, city, country) VALUES
('Indira Gandhi International Airport',   'Delhi',     'India'),
('Chhatrapati Shivaji Maharaj Airport',    'Mumbai',    'India'),
('Kempegowda International Airport',       'Bangalore', 'India'),
('Rajiv Gandhi International Airport',     'Hyderabad', 'India'),
('Netaji Subhas Chandra Bose Airport',     'Kolkata',   'India'),
('Chennai International Airport',          'Chennai',   'India');

-- Sample flights
INSERT INTO FLIGHT (airline_id, flight_number, source_airport, destination_airport, departure_time, arrival_time, total_seats, available_seats) VALUES
(1, 'AI-101', 1, 2, '2026-04-01 06:00:00', '2026-04-01 08:15:00', 180, 180),
(1, 'AI-102', 2, 1, '2026-04-01 10:00:00', '2026-04-01 12:15:00', 180, 180),
(2, '6E-201', 1, 3, '2026-04-01 07:30:00', '2026-04-01 10:15:00', 200, 200),
(2, '6E-202', 3, 1, '2026-04-01 14:00:00', '2026-04-01 16:45:00', 200, 200),
(3, 'SG-301', 2, 4, '2026-04-02 09:00:00', '2026-04-02 10:30:00', 160, 160),
(4, 'UK-401', 1, 6, '2026-04-02 11:00:00', '2026-04-02 13:45:00', 170, 170),
(5, 'G8-501', 5, 2, '2026-04-03 08:00:00', '2026-04-03 10:30:00', 150, 150);
