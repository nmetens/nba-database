""" Author: Nathan Metens

    * This file is the main.
    * In this file, I connect to the PSU server database
    * with login credentials that are environment variables
    * for safety purposes.
"""

# External Modules:
import os
import numpy as np
import nba_api.stats.static.players as p # Player list
from nba_api.stats.endpoints import playercareerstats # Player stats
from nba_api.stats.endpoints import TeamDetails # Team data

# My modules:
import database_connection as db
import insert as i

# Main method:
def main():
    # Setting up the connection to the database:
    db_name = 'spr25adb0047'
    db_user = 'spr25adb0047'
    db_password = os.environ['password'] # Getting my local environment var for privacy
    db_host = 'dbclass.cs.pdx.edu'
    db_port = 5432 

    conn = db.create_connection(db_name, db_user, db_password, db_host, db_port) # Returns a connection
    cursor = conn.cursor() # Get the cursor from the connection to execute queries

    nba_players = p.get_players() # Get all the NBA players
    active_players = [] # Empty list for active players

    # Create list of active players:
    for player in nba_players:
    	if player['is_active'] is True:
    		active_players.append(player)

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
       nba_id = i.get_player_id(player, active_players)

       # Get the career stats from the player id and create pandas datafram:
       nba_player = playercareerstats.PlayerCareerStats(player_id=f'{nba_id}')
       df = nba_player.get_data_frames()[0]

       insert_stmt, data = i.insert(df, 'Players')
       #cursor.execute(i.insert(df, 'Players')) # execute insert statement
       cursor.execute(insert_stmt, data)
       # Adding the player name in each row corresponding to the player_id:
       cursor.execute(f'UPDATE nba.Players SET full_name=\'{player}\' where player_id = {i.get_player_id(player, active_players)};')
       cursor.execute(f'update nba.Players set ppg=(pts/gp) where player_id={i.get_player_id(player, active_players)};')

    # Get all the teams from my favorite player's table:
    cursor.execute('select distinct team_id from nba.Players')
    team_ids = cursor.fetchall() # Collect the return of the query statement

    print(team_ids)

    # Loop through the team_ids returned from the previous query and collect
    # their information to add the team data to the nba.Teams table:
    for nba_team in team_ids:
        team = TeamDetails(team_id=nba_team)
        team_df = team.get_data_frames()[0]
        print(team_df)
        #team_df = team_df.replace({'nan':'NULL'}, inplace=True)

        insert_stmt, data = i.insert(team_df, 'Teams')
        cursor.execute(insert_stmt, data)
        print('insrted')

    cursor.close()
    conn.commit()

if __name__ == "__main__":
    main()
