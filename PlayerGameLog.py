from players import players
import insert as i

def player_game_log(cursor):
	for player in players:	
		nba_id = i.get_player_id(player)
		gamelog = PlayerGameLog(player_id=nba_id, season='2024-25')
		df = gamelog.get_data_frames()[0]
