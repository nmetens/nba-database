
from nba_api.stats.endpoints import TeamDetails# Team

#[(1610612744,), (1610612739,), (1610612738,), (1610612743,), (1610612757,), (1610612742,), (1610612750,), (1610612749,), (1610612760,)]
ids = [1610612744, 1610612739, 1610612738, 1610612743, 1610612757, 1610612742, 1610612750, 1610612749, 1610612760]

for i in ids:
	team = TeamDetails(team_id=i)
	df = team.get_data_frames()[0]
	df = df.astype(object)

	columns = ', '.join(df.columns)
	row_list = df.iloc[0].tolist()
	data = tuple(row_list)

	print(columns)
	print(data)
