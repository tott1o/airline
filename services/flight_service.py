"""
Flight Service — business logic for flights, airlines, and airports.
"""

from dao.flight_dao import FlightDAO


class FlightService:

    # ---- FLIGHTS ------------------------------------------------------

    @staticmethod
    def search_flights(source_airport_id, destination_airport_id):
        """Return available flights between two airports."""
        return FlightDAO.find_flights(source_airport_id, destination_airport_id)

    @staticmethod
    def get_all_flights():
        return FlightDAO.get_all_flights()

    @staticmethod
    def get_flight(flight_id):
        return FlightDAO.get_flight_by_id(flight_id)

    @staticmethod
    def add_flight(airline_id, flight_number, source_airport,
                   destination_airport, departure_time, arrival_time,
                   total_seats):
        return FlightDAO.insert_flight(
            airline_id, flight_number, source_airport, destination_airport,
            departure_time, arrival_time, total_seats, total_seats
        )

    @staticmethod
    def update_flight(flight_id, airline_id, flight_number, source_airport,
                      destination_airport, departure_time, arrival_time,
                      total_seats, available_seats):
        FlightDAO.update_flight(
            flight_id, airline_id, flight_number, source_airport,
            destination_airport, departure_time, arrival_time,
            total_seats, available_seats
        )

    @staticmethod
    def delete_flight(flight_id):
        FlightDAO.delete_flight(flight_id)

    # ---- AIRLINES -----------------------------------------------------

    @staticmethod
    def add_airline(name, code):
        return FlightDAO.insert_airline(name, code)

    @staticmethod
    def update_airline(airline_id, name, code):
        FlightDAO.update_airline(airline_id, name, code)

    @staticmethod
    def delete_airline(airline_id):
        FlightDAO.delete_airline(airline_id)

    @staticmethod
    def get_all_airlines():
        return FlightDAO.get_all_airlines()

    # ---- AIRPORTS -----------------------------------------------------

    @staticmethod
    def add_airport(name, city, country):
        return FlightDAO.insert_airport(name, city, country)

    @staticmethod
    def update_airport(airport_id, name, city, country):
        FlightDAO.update_airport(airport_id, name, city, country)

    @staticmethod
    def delete_airport(airport_id):
        FlightDAO.delete_airport(airport_id)

    @staticmethod
    def get_all_airports():
        return FlightDAO.get_all_airports()
