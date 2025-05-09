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
	
	"""
	"""
	# Testing:
	#dm.api_players()
	"""
	"""

	#db.query('drop_all.sql', cursor); print('All tables dropped')
	#db.query('create_all_tables.sql', cursor); print('All tables created')

	"""
	6 total tables are created:
	"""
	# 1) Create the nba.Seasons table:
	#dm.nba_seasons(cursor); print('NBA.Seasons table populated')

	# 2) Create the nba.Teams table: (this one takes the most tries)
	#dm.nba_teams(cursor); print('NBA.Teams table populated')

	# 3) Create the nba.Players table:
	cursor, conn = dm.nba_players(cursor, conn); print('NBA.Players table populated')

	# 4) Create the nba.Awards table:
	#dm.nba_awards(cursor); print('NBA.Awards table populated')

	# 5) Create the nba.CommonPlayerInfo table:
	#info.common_player_info(cursor); print('NBA.CommonPlayerInfo table populated')
	
	# 6) Create the nba.PlayerGameLog table:
	#log.player_game_log(cursor); print('NBA.PlayerGameLog table populated')

	cursor.close()
	conn.commit()

if __name__ == "__main__":
	main()
