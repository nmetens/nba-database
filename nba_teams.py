from nba_api.stats.endpoints import TeamDetails # Team data
import insert as i

def nba_teams(cursor):
	# Get all the teams from my favorite player's table:
	cursor.execute('select distinct team_id from nba.Players')
	team_ids = cursor.fetchall() # Collect the return of the query statement

	# Loop through the team_ids returned from the previous query and collect
	# their information to add the team data to the nba.Teams table:
	for nba_team in team_ids:
		team = TeamDetails(team_id=nba_team)
		team_df = team.get_data_frames()[0]
		print(team_df)
		#team_df = team_df.replace({'nan':'NULL'}, inplace=True)

		insert_stmt, data = i.insert(team_df, 'Teams')
		cursor.execute(insert_stmt, data)

	return cursor
