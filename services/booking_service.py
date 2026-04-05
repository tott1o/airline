"""
Booking Service — business logic for booking and cancellation.
"""

import random
import string

from dao.booking_dao import BookingDAO
from dao.flight_dao import FlightDAO


class BookingService:

    @staticmethod
    def _generate_seat_number():
        """Generate a random seat number like 12A, 7C, etc."""
        row = random.randint(1, 30)
        col = random.choice(string.ascii_uppercase[:6])  # A-F
        return f"{row}{col}"

    @staticmethod
    def book_flight(user_id, flight_id, passengers):
        """
        Book a flight for one or more passengers.

        Parameters
        ----------
        user_id : int
        flight_id : int
        passengers : list[dict]
            Each dict has keys: name, age, gender, passport_number

        Returns
        -------
        booking_id : int
        """
        # Check seat availability
        flight = FlightDAO.get_flight_by_id(flight_id)
        if not flight:
            raise ValueError("Flight not found.")
        if flight["available_seats"] < len(passengers):
            raise ValueError("Not enough seats available on this flight.")

        # Create booking
        booking_id = BookingDAO.insert_booking(user_id, flight_id)

        # Add each passenger
        for pax in passengers:
            passenger_id = BookingDAO.insert_passenger(
                pax["name"], pax["age"], pax["gender"], pax["passport_number"]
            )
            seat = BookingService._generate_seat_number()
            BookingDAO.insert_booking_passenger(booking_id, passenger_id, seat)

        # Decrease available seats
        FlightDAO.update_available_seats(flight_id, -len(passengers))

        return booking_id

    @staticmethod
    def cancel_booking(booking_id):
        """Cancel a booking and restore the seat count."""
        booking = BookingDAO.get_booking_by_id(booking_id)
        if not booking:
            raise ValueError("Booking not found.")
        if booking["booking_status"] == "Cancelled":
            raise ValueError("This booking is already cancelled.")

        # Count passengers to restore seats
        passengers = BookingDAO.get_passengers_for_booking(booking_id)
        FlightDAO.update_available_seats(booking["flight_id"], len(passengers))

        BookingDAO.update_booking_status(booking_id, "Cancelled")

    @staticmethod
    def get_booking_history(user_id):
        return BookingDAO.get_bookings_by_user(user_id)

    @staticmethod
    def get_all_bookings():
        return BookingDAO.get_all_bookings()

    @staticmethod
    def get_passengers(booking_id):
        return BookingDAO.get_passengers_for_booking(booking_id)
