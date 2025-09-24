import mysql.connector
from mysql.connector import MySQLConnection


def connect_db() -> MySQLConnection:
    """
    Establish and return a connection to the MySQL database.

    Update the password below to your actual MySQL root password before running.
    """
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin123",  # TODO: Replace with your actual MySQL root password
        database="fletapp",
    )


