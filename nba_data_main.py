""" Author: Nathan Metens

    * This file is the main.
    * In this file, I connect to the PSU server database
    * with login credentials that are environment variables
    * for safety purposes.
"""

# External Modules:
import os
import numpy as np
import nba_api.stats.static.players as p # Player list
from nba_api.stats.endpoints import playercareerstats # Player stats
from nba_api.stats.endpoints import TeamDetails # Team data
from nba_api.stats.endpoints import PlayerAwards

from nba_api.stats.endpoints import PlayerGameLog, CommonPlayerInfo, TeamGameLog, LeagueGameFinder

# My modules:
import database_connection as db
import insert as i
import nba_players as nba_p
import nba_teams as nba_t
import nba_awards as nba_a
import player_game_log as log
import common_player_info as info
import nba_seasons as nba_s

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

	# Create the nba.Seasons table:
	#nba_s.nba_seasons(cursor)

	# Create the nba.Teams table:
	#nba_t.nba_teams(cursor)

	# Create the nba.Players table:
	#nba_p.nba_players(cursor)

	# Create the nba.Awards table:
	#nba_a.nba_awards(cursor)

	# Create the nba.CommonPlayerInfo table:
	#info.common_player_info(cursor)	
	
	# Create the nba.PlayerGameLog table:
	log.player_game_log(cursor)

	cursor.close()
	conn.commit()

if __name__ == "__main__":
	main()
