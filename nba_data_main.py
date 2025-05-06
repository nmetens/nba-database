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

    players = p.get_players() # Get all the NBA players
    active_players = [] # Empty list for active players

    # Create list of active players:
    for player in players:
    	if player['is_active'] is True:
    		active_players.append(player)

    # Create a list of my favorite NBA players:
    players = [
        'Stephen Curry', 
        'LeBron James', 
        'Kyrie Irving', 
        'Kevin Durant', 
        'Damian Lillard',
        'Anthony Edwards',
        'Jayson Tatum',
        'Jalen Brunson',
        'Jamal Murray',
        'Giannis Antetokounmpo',
	'James Harden',
	'Klay Thompson'
    ]

    # Add a full_name column for the player name:
    cursor.execute('alter table nba.players add column full_name varchar(30);')

    for player in players:
       cursor.execute(i.insert_into_players(player, active_players)) # execute insert statement
       # Adding the player name in each row corresponding to the player_id:
       cursor.execute(f'UPDATE nba.Players SET full_name=\'{player}\' where player_id = {i.get_player_id(player, active_players)};')

    conn.commit()

if __name__ == "__main__":
    main()
