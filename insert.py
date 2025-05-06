import pandas as pd
from nba_api.stats.endpoints import playercareerstats # Player stats

# Get the id of the player in the active players list:
def get_player_id(name: str, active_players: list):
	for player in active_players:
		if player['full_name'] == name:
			return player['id']

def insert_into_players(player_name: str, active_players: list) -> str:
	# Get the id of a player by full_name:
	player_id = get_player_id(player_name, active_players)

	# Get the career stats from the player id and create pandas datafram:
	player = playercareerstats.PlayerCareerStats(player_id=f'{player_id}')
	df = player.get_data_frames()[0]
	df = df.astype(object)

	columns = ', '.join(df.columns) # columns separated by comma
	vals = ', '.join(['%s'] * len(df.columns)) # '%s' separated by cols * total cols

	row_list = df.iloc[0].tolist()     # get the first fow of data
	#row_list.append(player_name)
	data = tuple(row_list) 

	# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
	insert = ( # create insert statement:
		f'insert into nba.Players ({columns}) '
		f'values {data};'
	)
	return insert


