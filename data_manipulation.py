from nba_api.stats.endpoints import CommonPlayerInfo, PlayerGameLog, TeamDetails, playercareerstats, PlayerAwards
import nba_api.stats.static.players as p # Player list
from nba_api.stats.static import teams
from players import players
import insert as i

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

def get_text_data(file: str):
	with open(file, 'r') as data:
		lines = data.readlines()
		for line in lines:
			print(line)
	

def nba_players(cursor):
	# Insert into the player and team tables:
	active_players = p.get_active_players() # List for active players

	# Add a ppg column for each player:
	#cursor.execute('alter table nba.players add column ppg float;')
	# Add a full_name column for the player name:
	#cursor.execute('alter table nba.players add column full_name varchar(30);')

	# Loop through all my favorite players and insert their first season into
	# the nba.Players table in the database:
	#for player in players:
	index = 549
	for player in active_players[index:]:
		# Get the id of a player by full_name:
		player_name = player['full_name']
		nba_id = i.get_player_id(player_name)
		print(player_name, 'index:', index)

		#if nba_id is not None:
		# Get the career stats from the player id and create pandas datafram:
		nba_player = playercareerstats.PlayerCareerStats(player_id=f'{nba_id}')
		df = nba_player.get_data_frames()[0]

		insert_stmt, data = i.insert(df, 'Players')

		if insert_stmt is not None and data is not None:
			cursor.execute(insert_stmt, data)
			# Adding the player name in each row corresponding to the player_id:
			cursor.execute(
				'UPDATE nba.Players SET full_name=%s where player_id = %s;',
				(player_name, i.get_player_id(player_name))
			)
			cursor.execute(f'update nba.Players set ppg=(pts/gp) where player_id={i.get_player_id(player_name)};')

		# Store all the players we get from the api in data.txt:
		df.to_json('data.txt', mode='a', orient='records', lines=True)

		index += 1

	return cursor

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
