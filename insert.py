import pandas as pd
import nba_api.stats.static.players as p # Player list

def get_player_id(name: str):
	""" Get the player id from the API using the 
	player's full_name from the active_players list.
	"""
	active_players = p.get_active_players() # Get all the NBA players
	for player in active_players:
		if player['full_name'] == name:
			return player['id']
	return None

def insert(df, table: str):
	""" Given a pandas df and a tablename,
	we can create an insert statement for the 
	table and return it.
	"""
	df = df.astype(object)

	columns = ', '.join(df.columns) # Separates the data by comma
	placeholders = ', '.join(['%s'] * len(df.columns)) # Creates tuple with '%s' for each column
	row_list = df.iloc[0].tolist() # Gets all the data from a row in the df and turns it into a list
	data = tuple(row_list) # Turn list into tuple

	insert = ( # create insert statement:
		f'insert into nba.{table} ({columns}) '
		f'values ({placeholders});'
	)
	return insert, data 
