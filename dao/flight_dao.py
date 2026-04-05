"""
Data Access Object for FLIGHT, AIRLINE, and AIRPORT tables.
"""

from db.queries import execute_query, fetch_all, fetch_one


class FlightDAO:

    # ---- FLIGHT -------------------------------------------------------

    @staticmethod
    def insert_flight(airline_id, flight_number, source_airport,
                      destination_airport, departure_time, arrival_time,
                      total_seats, available_seats):
        sql = """INSERT INTO FLIGHT
                 (airline_id, flight_number, source_airport, destination_airport,
                  departure_time, arrival_time, total_seats, available_seats)
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""
        return execute_query(sql, (airline_id, flight_number, source_airport,
                                   destination_airport, departure_time,
                                   arrival_time, total_seats, available_seats))

    @staticmethod
    def update_flight(flight_id, airline_id, flight_number, source_airport,
                      destination_airport, departure_time, arrival_time,
                      total_seats, available_seats):
        sql = """UPDATE FLIGHT SET airline_id=%s, flight_number=%s,
                 source_airport=%s, destination_airport=%s,
                 departure_time=%s, arrival_time=%s,
                 total_seats=%s, available_seats=%s
                 WHERE flight_id=%s"""
        execute_query(sql, (airline_id, flight_number, source_airport,
                            destination_airport, departure_time, arrival_time,
                            total_seats, available_seats, flight_id))

    @staticmethod
    def delete_flight(flight_id):
        execute_query("DELETE FROM FLIGHT WHERE flight_id = %s", (flight_id,))

    @staticmethod
    def get_all_flights():
        sql = """SELECT f.*, a.airline_name, a.airline_code,
                        src.city AS source_city, dst.city AS destination_city
                 FROM FLIGHT f
                 JOIN AIRLINE a  ON f.airline_id = a.airline_id
                 JOIN AIRPORT src ON f.source_airport = src.airport_id
                 JOIN AIRPORT dst ON f.destination_airport = dst.airport_id
                 ORDER BY f.departure_time"""
        return fetch_all(sql)

    @staticmethod
    def get_flight_by_id(flight_id):
        sql = """SELECT f.*, a.airline_name, a.airline_code,
                        src.city AS source_city, dst.city AS destination_city
                 FROM FLIGHT f
                 JOIN AIRLINE a  ON f.airline_id = a.airline_id
                 JOIN AIRPORT src ON f.source_airport = src.airport_id
                 JOIN AIRPORT dst ON f.destination_airport = dst.airport_id
                 WHERE f.flight_id = %s"""
        return fetch_one(sql, (flight_id,))

    @staticmethod
    def find_flights(source_airport_id, destination_airport_id):
        sql = """SELECT f.*, a.airline_name, a.airline_code,
                        src.city AS source_city, dst.city AS destination_city
                 FROM FLIGHT f
                 JOIN AIRLINE a  ON f.airline_id = a.airline_id
                 JOIN AIRPORT src ON f.source_airport = src.airport_id
                 JOIN AIRPORT dst ON f.destination_airport = dst.airport_id
                 WHERE f.source_airport = %s AND f.destination_airport = %s
                   AND f.available_seats > 0
                 ORDER BY f.departure_time"""
        return fetch_all(sql, (source_airport_id, destination_airport_id))

    @staticmethod
    def update_available_seats(flight_id, delta):
        """Increase (positive delta) or decrease (negative delta) available seats."""
        sql = "UPDATE FLIGHT SET available_seats = available_seats + %s WHERE flight_id = %s"
        execute_query(sql, (delta, flight_id))

    # ---- AIRLINE ------------------------------------------------------

    @staticmethod
    def insert_airline(airline_name, airline_code):
        sql = "INSERT INTO AIRLINE (airline_name, airline_code) VALUES (%s, %s)"
        return execute_query(sql, (airline_name, airline_code))

    @staticmethod
    def update_airline(airline_id, airline_name, airline_code):
        sql = "UPDATE AIRLINE SET airline_name=%s, airline_code=%s WHERE airline_id=%s"
        execute_query(sql, (airline_name, airline_code, airline_id))

    @staticmethod
    def delete_airline(airline_id):
        execute_query("DELETE FROM AIRLINE WHERE airline_id = %s", (airline_id,))

    @staticmethod
    def get_all_airlines():
        return fetch_all("SELECT * FROM AIRLINE ORDER BY airline_name")

    # ---- AIRPORT ------------------------------------------------------

    @staticmethod
    def insert_airport(airport_name, city, country):
        sql = "INSERT INTO AIRPORT (airport_name, city, country) VALUES (%s, %s, %s)"
        return execute_query(sql, (airport_name, city, country))

    @staticmethod
    def update_airport(airport_id, airport_name, city, country):
        sql = "UPDATE AIRPORT SET airport_name=%s, city=%s, country=%s WHERE airport_id=%s"
        execute_query(sql, (airport_name, city, country, airport_id))

    @staticmethod
    def delete_airport(airport_id):
        execute_query("DELETE FROM AIRPORT WHERE airport_id = %s", (airport_id,))

    @staticmethod
    def get_all_airports():
        return fetch_all("SELECT * FROM AIRPORT ORDER BY city")
