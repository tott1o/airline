"""
Data Access Object for the USERS table.
"""

from db.queries import execute_query, fetch_all, fetch_one


class UserDAO:

    @staticmethod
    def insert_user(name, email, password, phone, role="customer"):
        sql = """INSERT INTO USERS (name, email, password, phone, role)
                 VALUES (%s, %s, %s, %s, %s)"""
        return execute_query(sql, (name, email, password, phone, role))

    @staticmethod
    def find_by_email(email):
        sql = "SELECT * FROM USERS WHERE email = %s"
        return fetch_one(sql, (email,))

    @staticmethod
    def find_by_id(user_id):
        sql = "SELECT * FROM USERS WHERE user_id = %s"
        return fetch_one(sql, (user_id,))

    @staticmethod
    def get_all():
        return fetch_all("SELECT * FROM USERS")
