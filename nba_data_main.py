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

# Main method:
def main():
    # Setting up the connection to the database:
    db_name = 'spr25adb0047'
    db_user = 'spr25adb0047'
    db_password = os.environ['password'] # Getting my local environment var for privacy
    db_host = 'dbclass.cs.pdx.edu'
    db_port = 5432 

    conn = db.create_connection(db_name, db_user, db_password, db_host, db_port) # Returns a connection

    # Source: https://www.freecodecamp.org/news/postgresql-in-python/
    cursor = conn.cursor() # Get the cursor from the connection to execute queries

    # Execute a query on the database connection:
    cursor.execute("SELECT * FROM spy.agent WHERE agent_id = 1")

    agent1 = cursor.fetchone()
    print(agent1)

    # Create the Player table:
    #cursor.execute

if __name__ == "__main__":
    main()
