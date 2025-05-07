from nba_api.stats.endpoints import PlayerGameLog
from players import players
import insert as i

def player_game_log(cursor):
	for player in players:	
		nba_id = i.get_player_id(player)
		gamelog = PlayerGameLog(player_id=nba_id, season='2024-25')
		df = gamelog.get_data_frames()[0]
		insert_stmt, data = i.insert(df, 'PlayerGameLog')
		cursor.execute(insert_stmt, data)
	return cursor

