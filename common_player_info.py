from nba_api.stats.endpoints import CommonPlayerInfo
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
