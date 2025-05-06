import pandas as pd

# Get the id of the player in the active players list:
def get_player_id(name: str, active_players: list):
	for player in active_players:
		if player['full_name'] == name:
			return player['id']

def insert(df, table: str):
	""" Given a pandas df and a tablename,
	we can create an insert statement for the 
	table and return it.
	"""

	df = df.astype(object)

	columns = ', '.join(df.columns)
	row_list = df.iloc[0].tolist()
	data = tuple(row_list)

	# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
	insert = ( # create insert statement:
		f'insert into nba.{table} ({columns}) '
		f'values {data};'
	)
	return insert

