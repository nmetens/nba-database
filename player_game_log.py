from nba_api.stats.endpoints import PlayerGameLog
from players import players
import insert as i

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
	for player in players:	
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
