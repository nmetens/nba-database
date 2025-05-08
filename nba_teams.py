from nba_api.stats.endpoints import TeamDetails # Team data
from nba_api.stats.endpoints import playercareerstats as ps # Player stats 
import insert as i
from players import players

from nba_api.stats.static import teams

def nba_teams(cursor):
	# Get all NBA teams
	nba_teams = teams.get_teams()

	# Extract team IDs and names
	team_ids = [(team['id'], team['full_name']) for team in nba_teams]
	
	# Get all the teams from my favorite player's table:
	#cursor.execute('select distinct team_id from nba.Players')
	#team_ids = cursor.fetchall() # Collect the return of the query statement

	# Loop through the team_ids returned from the previous query and collect
	# their information to add the team data to the nba.Teams table:
	for nba_team in team_ids:
		team = TeamDetails(team_id=nba_team[0])
		team_df = team.get_data_frames()[0]
		print(team_df)

		insert_stmt, data = i.insert(team_df, 'Teams')
		cursor.execute(insert_stmt, data)

	return cursor
