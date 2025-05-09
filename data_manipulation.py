from nba_api.stats.endpoints import CommonPlayerInfo, PlayerGameLog, TeamDetails, playercareerstats, PlayerAwards
import nba_api.stats.static.players as p # Player list
from nba_api.stats.static import teams
from players import players
import insert as i

import pandas as pd
import json

import os
from pathlib import Path

def common_player_info(cursor):
	for player in players:
		nba_id = i.get_player_id(player)
		player_info = CommonPlayerInfo(player_id=nba_id)
		df = player_info.get_data_frames()[0]
		insert_stmt, data = i.insert(df, 'CommonPlayerInfo')
		cursor.execute(insert_stmt, data)
	return cursor

def nba_awards(cursor):
	cursor.execute('select player_id from nba.Players;')
	nba_player_ids = cursor.fetchall()
	print(nba_player_ids)

	for p_id in nba_player_ids:
		award = PlayerAwards(player_id=p_id)
		df = award.get_data_frames()[0]

		insert_stmt, data = i.insert(df, 'Awards')
		cursor.execute(insert_stmt, data)

	return cursor

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

def api_players():
	"""
	Putting all the data in the api return into a text file.
	The API consistently stalls, and manually changing the index
	is laborous.
	"""
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
	
def list_to_df(json_lines: list) -> pd.DataFrame:
	data_dicts = [json.loads(line) for line in json_lines]
	return pd.DataFrame(data_dicts)

def nba_players(cursor, conn):
	data = clean_data('player_data.txt')
	df = list_to_df(data)


	# Add a ppg column for each player:
	cursor.execute('alter table nba.players add column ppg float;')
	# Add a full_name column for the player name:
	cursor.execute('alter table nba.players add column full_name varchar(30);')

	id_list = []

	for index, row in df.iterrows():
		player_id = row['PLAYER_ID']
		print(player_id)

		if player_id not in id_list:
			id_list.append(player_id)

			player_name = i.get_player_name(player_id)

			current_row = pd.DataFrame([row])
			insert_stmt, data = i.insert(current_row, 'Players')

			if insert_stmt and data:
				cursor.execute(insert_stmt, data)
				cursor.execute(
					'UPDATE nba.Players SET full_name=%s where player_id = %s;',
					(player_name, player_id)
				)
				cursor.execute(
					'update nba.Players set ppg=pts/NULLIF(gp, 0) where player_id=%s;',
					(player_id,)
				)
		conn.commit()

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

def nba_teams(cursor):
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
		cursor.execute(insert_stmt, data)
		index += 1
		
		# Store all the teams we get from the api in team_data.txt,
		# since the api times out on most occasions:
		team_df.to_json('team_data.txt', mode='a', orient='records', lines=True)

	return cursor

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

def player_game_log(cursor):
	active_players = p.get_active_players() # List for active players
	for player in active_players:	
		nba_id = i.get_player_id(player)

		season_id = '2024-25'
		gamelog = PlayerGameLog(player_id=nba_id, season=season_id)
		df = gamelog.get_data_frames()[0]

		# Replace 'SEASON_ID' in the dataframe to match your DB format
		# All season_id's in the df are '22024'. Revert to '2024-25':
		df['SEASON_ID'] = df['SEASON_ID'].apply(revert_season_id)
		
		insert_stmt, data = i.insert(df, 'PlayerGameLogs')
		cursor.execute(insert_stmt, data)

	return cursor

def player_game_log(cursor):
	
	active_players = p.get_active_players() # List for active players
	for player in active_players:	
		nba_id = i.get_player_id(player)
		gamelog = PlayerGameLog(player_id=nba_id, season='2024-25')
		df = gamelog.get_data_frames()[0]
