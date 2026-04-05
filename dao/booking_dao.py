"""
Data Access Object for BOOKING, BOOKING_PASSENGER, and PASSENGER tables.
"""

from db.queries import execute_query, fetch_all, fetch_one


class BookingDAO:

    # ---- BOOKING ------------------------------------------------------

    @staticmethod
    def insert_booking(user_id, flight_id):
        sql = """INSERT INTO BOOKING (user_id, flight_id, booking_date, booking_status)
                 VALUES (%s, %s, NOW(), 'Confirmed')"""
        return execute_query(sql, (user_id, flight_id))

    @staticmethod
    def update_booking_status(booking_id, status):
        sql = "UPDATE BOOKING SET booking_status = %s WHERE booking_id = %s"
        execute_query(sql, (status, booking_id))

    @staticmethod
    def get_booking_by_id(booking_id):
        sql = """SELECT b.*, f.flight_number, a.airline_name,
                        src.city AS source_city, dst.city AS destination_city,
                        f.departure_time, f.arrival_time
                 FROM BOOKING b
                 JOIN FLIGHT f   ON b.flight_id = f.flight_id
                 JOIN AIRLINE a  ON f.airline_id = a.airline_id
                 JOIN AIRPORT src ON f.source_airport = src.airport_id
                 JOIN AIRPORT dst ON f.destination_airport = dst.airport_id
                 WHERE b.booking_id = %s"""
        return fetch_one(sql, (booking_id,))

    @staticmethod
    def get_bookings_by_user(user_id):
        sql = """SELECT b.*, f.flight_number, a.airline_name,
                        src.city AS source_city, dst.city AS destination_city,
                        f.departure_time, f.arrival_time
                 FROM BOOKING b
                 JOIN FLIGHT f   ON b.flight_id = f.flight_id
                 JOIN AIRLINE a  ON f.airline_id = a.airline_id
                 JOIN AIRPORT src ON f.source_airport = src.airport_id
                 JOIN AIRPORT dst ON f.destination_airport = dst.airport_id
                 WHERE b.user_id = %s
                 ORDER BY b.booking_date DESC"""
        return fetch_all(sql, (user_id,))

    @staticmethod
    def get_all_bookings():
        sql = """SELECT b.*, u.name AS user_name, u.email,
                        f.flight_number, a.airline_name,
                        src.city AS source_city, dst.city AS destination_city,
                        f.departure_time, f.arrival_time
                 FROM BOOKING b
                 JOIN USERS u    ON b.user_id = u.user_id
                 JOIN FLIGHT f   ON b.flight_id = f.flight_id
                 JOIN AIRLINE a  ON f.airline_id = a.airline_id
                 JOIN AIRPORT src ON f.source_airport = src.airport_id
                 JOIN AIRPORT dst ON f.destination_airport = dst.airport_id
                 ORDER BY b.booking_date DESC"""
        return fetch_all(sql)

    # ---- PASSENGER ----------------------------------------------------

    @staticmethod
    def insert_passenger(name, age, gender, passport_number):
        sql = """INSERT INTO PASSENGER (name, age, gender, passport_number)
                 VALUES (%s, %s, %s, %s)"""
        return execute_query(sql, (name, age, gender, passport_number))

    @staticmethod
    def get_passengers_for_booking(booking_id):
        sql = """SELECT p.*, bp.seat_number
                 FROM BOOKING_PASSENGER bp
                 JOIN PASSENGER p ON bp.passenger_id = p.passenger_id
                 WHERE bp.booking_id = %s"""
        return fetch_all(sql, (booking_id,))

    # ---- BOOKING_PASSENGER --------------------------------------------

    @staticmethod
    def insert_booking_passenger(booking_id, passenger_id, seat_number):
        sql = """INSERT INTO BOOKING_PASSENGER (booking_id, passenger_id, seat_number)
                 VALUES (%s, %s, %s)"""
        return execute_query(sql, (booking_id, passenger_id, seat_number))
