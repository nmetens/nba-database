""" Author: Nathan Metens

    * This file is the main.
    * In this file, I connect to the PSU server database
    * with login credentials that are environment variables
    * for safety purposes.
"""

# External Modules:
import os
import nba_api.stats.static.players as p # Player list

# My modules:
import database_connection as db
import insert as i

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

    players = p.get_players()
    active_players = []
    # Create list of acticve players:
    for player in players:
    	if player['is_active'] is True:
    		active_players.append(player)

    # create a list of fav players:
    players = ['Stephen Curry', 'LeBron James', 'Kyrie Irving', 'Kevin Durant', 'Damian Lillard']
    for player in players:
       cursor.execute(i.insert_into_players(player, active_players)) # execute insert statement

    conn.commit()

if __name__ == "__main__":
    main()
