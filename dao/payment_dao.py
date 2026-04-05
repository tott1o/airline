"""
Data Access Object for the PAYMENT table.
"""

from db.queries import execute_query, fetch_all, fetch_one


class PaymentDAO:

    @staticmethod
    def insert_payment(booking_id, amount, payment_method):
        sql = """INSERT INTO PAYMENT (booking_id, amount, payment_date,
                 payment_method, payment_status)
                 VALUES (%s, %s, NOW(), %s, 'Completed')"""
        return execute_query(sql, (booking_id, amount, payment_method))

    @staticmethod
    def get_payment_by_booking(booking_id):
        sql = "SELECT * FROM PAYMENT WHERE booking_id = %s"
        return fetch_one(sql, (booking_id,))

    @staticmethod
    def get_all_payments():
        return fetch_all("SELECT * FROM PAYMENT ORDER BY payment_date DESC")
