""" Author: Nathan Metens

    * This file is the main.
    * In this file, I connect to the PSU server database
    * with login credentials that are environment variables
    * for safety purposes.
"""

# External Modules:
import os
import numpy as np

# My modules:
import data_manipulation as dm
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
	
	#db.query('drop_all.sql', cursor); print('All tables dropped')
	#db.query('create_all_tables.sql', cursor); print('All tables created')

	"""
	6 total tables are created:
	"""
	# 1) Create the nba.Seasons table:
	#dm.nba_seasons(cursor); print('NBA.Seasons table populated')

	# 2) Create the nba.Teams table: (this one takes the most tries)
	#cursor, conn = dm.nba_teams(cursor, conn); print('NBA.Teams table populated')

	# 3) Create the nba.PlayerInfo table:
	#cursor, conn = dm.nba_players(cursor, conn); print('NBA.Players table populated')

	# 4) Create the nba.Awards table:
	#cursor, conn = dm.nba_awards(cursor, conn); print('NBA.Awards table populated')

	# 5) Create the nba.PlayersStats table:
	#cursor, conn = dm.player_stats(cursor, conn); print('NBA.PlayersStats table populated')
	
	# 6) Create the nba.PlayerGameLog table:
	cursor, conn = dm.player_game_log(cursor, conn); print('NBA.PlayerGameLog table populated')

	cursor.close()
	conn.commit()

if __name__ == "__main__":
	main()
