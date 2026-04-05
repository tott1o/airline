"""
Database connection helper.
Returns a new MySQL connection using settings from config.py.
"""

import mysql.connector
from config import DB_CONFIG


def get_connection():
    """Create and return a new MySQL database connection."""
    return mysql.connector.connect(**DB_CONFIG)
