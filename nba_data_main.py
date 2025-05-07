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

	# Generate season IDs from 1996-97 to 2024-25 (ChatGpt)
	season_ids = []
	for start_year in range(1996, 2025):
	    end_year_short = str(start_year + 1)[-2:]  # get last two digits
	    season_id = f"{start_year}-{end_year_short}"
	    season_ids.append((season_id, start_year, start_year + 1))

	for season in season_ids:
		cursor.execute(
			'insert into nba.Seasons (season_id, start_year, end_year) values (%s, %s, %s);',
			(season[0], season[1], season[2])
		)

	# Create the nba.Players table:
	#nba_p.nba_players(cursor)

	# Create the nba.Teams table:
	#nba_t.nba_teams(cursor)

	# Create the nba.Awards table:
	#nba_a.nba_awards(cursor)

	# Create the nba.PlayerGameLog table:
	#log.player_game_log(cursor)

	# Create the nba.CommonPlayerInfo table:
	#info.common_player_info(cursor)	
	
	cursor.close()
	conn.commit()

if __name__ == "__main__":
	main()
