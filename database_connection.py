""" Author: Nathan Metens
    * This module has the method to connect
    * to the database on the PSU server.
"""
import psycopg2
from psycopg2 import OperationalError
import logging

# Method to connect to the PSU server database with environment variable credentials:
def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        logging.info("Connection to PostgreSQL DB successful")
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        logging.error(f"OperationalError: {e}")
        print("Connection to PostgreSQL DB successful")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        print("Connection to PostgreSQL DB successful")
    return connection
