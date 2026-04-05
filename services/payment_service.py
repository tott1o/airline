"""
Payment Service — business logic for recording payments.
"""

from dao.payment_dao import PaymentDAO


class PaymentService:

    @staticmethod
    def record_payment(booking_id, amount, payment_method):
        """Record a payment for a booking. Returns payment_id."""
        return PaymentDAO.insert_payment(booking_id, amount, payment_method)

    @staticmethod
    def get_payment(booking_id):
        """Get payment details for a booking."""
        return PaymentDAO.get_payment_by_booking(booking_id)
