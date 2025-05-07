import nba_api.stats.static.players as p # Player list
from nba_api.stats.endpoints import playercareerstats # Player stats
import insert as i

def nba_players(cursor):
	# Insert into the player and team tables:
	active_players = p.get_active_players() # List for active players

	# Create a list of my favorite NBA players:
	players = [
		'Stephen Curry', 
		'LeBron James', 
		'Kyrie Irving', 
		'Kevin Durant', 
		'Damian Lillard',
		'Anthony Edwards',
		'Jayson Tatum',
		'Jalen Brunson',
		'Jamal Murray',
		'Giannis Antetokounmpo',
		'James Harden',
		'Klay Thompson'
	]

	# Add a ppg column for each player:
	cursor.execute('alter table nba.players add column ppg float;')
	# Add a full_name column for the player name:
	cursor.execute('alter table nba.players add column full_name varchar(30);')

	# Loop through all my favorite players and insert their first season into
	# the nba.Players table in the database:
	for player in players:
		# Get the id of a player by full_name:
		nba_id = i.get_player_id(player)
		print(nba_id)

		# Get the career stats from the player id and create pandas datafram:
		nba_player = playercareerstats.PlayerCareerStats(player_id=f'{nba_id}')
		df = nba_player.get_data_frames()[0]

		insert_stmt, data = i.insert(df, 'Players')
		#cursor.execute(i.insert(df, 'Players')) # execute insert statement
		cursor.execute(insert_stmt, data)
		# Adding the player name in each row corresponding to the player_id:
		cursor.execute(f'UPDATE nba.Players SET full_name=\'{player}\' where player_id = {i.get_player_id(player)};')
		cursor.execute(f'update nba.Players set ppg=(pts/gp) where player_id={i.get_player_id(player)};')

	return cursor
