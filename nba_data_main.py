""" Author: Nathan Metens

    * This file is the main.
    * In this file, I connect to the PSU server database
    * with login credentials that are environment variables
    * for safety purposes.
"""

# External Modules:
import os

# My modules:
import database_connection as db

# Query method:
def query(file, cursor):
    """ 
        Arguments
        file: the name of the sql file that holds the query.
        cursor: the cursor connected to the databse.

        Opens a file for reading. Makes the contents of the file
        an sql query that is executed by the cursor in the database: 

        Returns the cursor object.
    """
    try:
        with open(file, 'r') as query:
            sql = query.read()	
            cursor.execute(sql)
    except Exception as e:
        print(f"Error executing query: {e}") 
    return cursor

# Main method:
def main():
    # Setting up the connection to the database:
    db_name = 'spr25adb0047'
    db_user = 'spr25adb0047'
    db_password = os.environ['password'] # Getting my local environment var for privacy
    db_host = 'dbclass.cs.pdx.edu'
    db_port = 5432 

    conn = db.create_connection(db_name, db_user, db_password, db_host, db_port) # Returns a connection
    cursor = conn.cursor() # Get the cursor from the connection to execute queries

    """
    agent1 = cursor.fetchone()
    print(agent1)
    """

    # Call query method to execute a query:
    query('create_players.sql', cursor)

    conn.commit()

if __name__ == "__main__":
    main()
