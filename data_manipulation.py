from nba_api.stats.endpoints import CommonPlayerInfo, PlayerGameLog, TeamDetails, playercareerstats, PlayerAwards
import nba_api.stats.static.players as p # Player list
from nba_api.stats.static import teams
from players import players
import insert as i

import pandas as pd
import json

import os
from pathlib import Path

def player_stats(cursor, conn):
	index = 16 # update the index when stall occurs
	for player in players[index:]:
		player_id = i.get_player_id(player)
		player_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
		df = player_stats.get_data_frames()[0]

		df = df[df['TEAM_ID'] != 0]  # Option 1: Drop the rows of team_id == 0

		insert_stmt, data = i.insert(df, 'PlayersStats')
		cursor.executemany(insert_stmt, data)
		print(player_id, "index:", index)

		conn.commit()

		index += 1
	return cursor, conn

def nba_awards(cursor, conn):
	cursor.execute('select person_id from nba.PlayerInfo;')
	nba_player_ids = cursor.fetchall()
	print(nba_player_ids)

	index = 25 # update when stalls
	for p_id in nba_player_ids[index:]:
		award = PlayerAwards(player_id=p_id)
		df = award.get_data_frames()[0]
		print(df, 'player_index:', index)
		df = df.replace([r'^\s*$', r'(?i)\(null\)', r'(?i)null'], None, regex=True)# Replace empty strings with None ChatGPT

		insert_stmt, data = i.insert(df, 'Awards')
		cursor.executemany(insert_stmt, data)
		conn.commit()
		index += 1

	return cursor, conn

def get_text_data(file: str) -> list:
	player_data = []
	with open(file, 'r') as data:
		lines = data.readlines()
		for line in lines:
			player_data.append(line)	
	return player_data 

def clean_data(file: str) -> list:
	data = get_text_data(file)
	cleaned_lines = [line.strip() for line in data if line.strip() and not line.strip().isdigit()]
	return cleaned_lines
"""
def api_players():
	"
	Putting all the data in the api return into a text file.
	The API consistently stalls, and manually changing the index
	is laborous.
	"
	active_players = p.get_active_players() # List for active players

	player_index = 0 # Go from 0 the len of the active_player list (549)
	# Method 1: Using os.path.exists()
	player_file = 'player_data.txt'
	if os.path.exists(player_file):
		# File exists. Get the last index we left off at before
		# API crash:
		with open(player_file, 'r') as file: 
			lines = file.readlines()
			if lines:
				player_index = int(lines[-1].rstrip('\n')) + 1
				print('left off on index:', player_index)
			else:
				player_index = 0

	# Loop through active_players and insert their data into
	# the player_data.txt:
		
	for player in active_players[player_index:]:
		# Get the id of a player by full_name:
		player_name = player['full_name']
		nba_id = i.get_player_id(player_name)
		print(player_name, 'player_index:', player_index)

		# Get the career stats from the player id and create pandas datafram:
		nba_player = playercareerstats.PlayerCareerStats(player_id=f'{nba_id}')
		df = nba_player.get_data_frames()[0]

		# Store all the players we get from the api in data.txt:
		df.to_json('player_data.txt', mode='a', orient='records', lines=True)

		with open('player_data.txt', 'a') as file:
			file.write(f'{player_index}\n')
		player_index += 1
"""
	
def list_to_df(json_lines: list) -> pd.DataFrame:
	data_dicts = [json.loads(line) for line in json_lines]
	return pd.DataFrame(data_dicts)

def nba_players(cursor, conn):
	
	index = 19 # change if stall occures
	for player_name in players[index:]:
		player_id = i.get_player_id(player_name)
		player_info = CommonPlayerInfo(player_id=player_id)
		print(player_id)
		
		# Get the player info the player id and create pandas datafram:
		df = player_info.get_data_frames()[0] # Get all the player data for their career in a dataframe

		print(df, 'index:', index)

		insert_stmt, data = i.insert(df, 'PlayerInfo')

		if insert_stmt and data:
			cursor.executemany(insert_stmt, data) # Many executes since there are multiple rows
		
		conn.commit() # Commit the insert after each player

		index += 1

	return cursor, conn

def nba_seasons(cursor):
	# Generate season IDs from 1996-97 to 2024-25 (ChatGpt)
	for start_year in range(1996, 2025):
		end_year_short = str(start_year + 1)[-2:]  # get last two digits
		season_id = f"{start_year}-{end_year_short}"

		cursor.execute(
			'insert into nba.Seasons (season_id, start_year, end_year) values (%s, %s, %s);',
			(season_id, start_year, start_year + 1)
		)	

	return cursor

def nba_teams(cursor, conn):
	# Get all NBA teams
	nba_teams = teams.get_teams()

	# Extract team IDs and names
	team_ids = [(team['id'], team['full_name']) for team in nba_teams]
	
	index = 0 # 0, 16
	for nba_team in team_ids[index:]:
		team = TeamDetails(team_id=nba_team[0])
		team_df = team.get_data_frames()[0]
		print(team_df, 'index:', index)

		insert_stmt, data = i.insert(team_df, 'Teams')
		if insert_stmt and data:
			cursor.executemany(insert_stmt, data)
		index += 1

		conn.commit()
		
	return cursor, conn

def convert_season_id(season_id: str) -> str:
	""" 
	Example season_id from nba.Seasons table: '2023-24', '2011-12'.
	2009-10 is the first game log year.

	Funtion splits the id into '2023' and '24'. Keep the year ('2023').
	Then add '2' in front of it: '22023':
	""" 
	return '2' + season_id.split('-')[0]

def revert_season_id(season_id: str) -> str:
	"""
	Example input: 22024
	Example output: 2024-25
	"""
	szn_id = (season_id[1:]) # 2024
	end_year = str(int(szn_id[2:]) + 1) # 24 + 1 = 25
	return szn_id + '-' + end_year # 2024-25

def player_game_log(cursor, conn):
	index = 29 # update after stall
	for player in players[index:]:	
		player_id = i.get_player_id(player)

		season_id = '2024-25'
		gamelog = PlayerGameLog(player_id=player_id, season=season_id)
		df = gamelog.get_data_frames()[0]

		# Replace 'SEASON_ID' in the dataframe to match your DB format
		# All season_id's in the df are '22024'. Revert to '2024-25':
		df['SEASON_ID'] = df['SEASON_ID'].apply(revert_season_id)
		
		insert_stmt, data = i.insert(df, 'PlayerGameLogs')
		cursor.executemany(insert_stmt, data)
		print(df, "index:", index)
		conn.commit()
		index += 1

	return cursor, conn
