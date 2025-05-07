import nba_api.stats.static.players as p # Player list
from nba_api.stats.endpoints import playercareerstats # Player stats
from nba_api.stats.endpoints import TeamDetails # Team data
from nba_api.stats.endpoints import PlayerAwards

import insert as i

nba_players = p.get_active_players() # Get all the NBA players

#for player in nba_players:
#	print(player)

players = [ #players of interest
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
'Klay Thompson',
'Jordan Poole',
'Ja Morant'
]

for player in players:
	nba_id = i.get_player_id(player, nba_players)

	nba_player = playercareerstats.PlayerCareerStats(player_id=f'{nba_id}')

	df = nba_player.get_data_frames()[0]
	df = df.astype(object)

print(df.head)

cols = [col.lower() for col in df.columns[:6]]
print(cols) # ['player_id', 'season_id', 'league_id', 'team_id', 'team_abbreviation', 'player_age']
cols = [cols[0], cols[-1]] # Chatgpt
print(cols)

print(df[cols[1].upper()])

"""
for nba_team in team_ids:
	team = TeamDetails(team_id=nba_team)
	team_df = team.get_data_frames()[0]
	print(team_df)
	#team_df = team_df.replace({'nan':'NULL'}, inplace=True)

	insert_stmt, data = i.insert(team_df, 'Teams')
	cursor.execute(insert_stmt, data)
	print('insrted')

for p_id in nba_player_ids:
	award = PlayerAwards(player_id=p_id)
	df = award.get_data_frames()[0]

	insert_stmt, data = i.insert(df, 'Awards')
	cursor.execute(insert_stmt, data)

"""
"""
"""
