"""
Generic query helpers used by DAO classes.
Each function obtains its own connection and closes it when done.
"""

from db.connection import get_connection


def execute_query(sql, params=None):
    """Execute an INSERT / UPDATE / DELETE and return the lastrowid."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(sql, params or ())
        conn.commit()
        return cursor.lastrowid
    finally:
        cursor.close()
        conn.close()


def fetch_all(sql, params=None):
    """Execute a SELECT and return all rows as a list of dicts."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params or ())
        return cursor.fetchall()
    finally:
        cursor.close()
        conn.close()


def fetch_one(sql, params=None):
    """Execute a SELECT and return a single row as a dict (or None)."""
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(sql, params or ())
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()
