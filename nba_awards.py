from nba_api.stats.endpoints import PlayerAwards
import insert as i

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
