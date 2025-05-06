""" Author: Nathan Metens

    * This file is the main.
    * In this file, I connect to the PSU server database
    * with login credentials that are environment variables
    * for safety purposes.
"""

# External Modules:
import os
import nba_api.stats.static.players as p # Player list
from nba_api.stats.endpoints import playercareerstats # Player stats

# My modules:
import database_connection as db

# Query method:
def query(file, cursor):
    """ 
        Arguments
        file: the name of the sql file that holds the query.
        cursor: the cursor connected to the databse.

        Opens a file for reading. Makes the contents of the file
        an sql query that is executed by the cursor in the database: 

        Returns the cursor object.
    """
    try:
        with open(file, 'r') as query:
            sql = query.read()	
            cursor.execute(sql)
    except Exception as e:
        print(f"Error executing query: {e}") 
    return cursor

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

    """
    agent1 = cursor.fetchone()
    print(agent1)
    """

    # Call query method to execute a query:
    #query('create_players.sql', cursor)

    players = p.get_players()
    active_players = []
    # Create list of acticve players:
    for player in players:
    	if player['is_active'] is True:
    		active_players.append(player)

    # Get the id of the player in the active players list:
    def get_player_id(name: str, active_players: list):
    	for player in active_players:
    		if player['full_name'] == name:
    			return player['id']

    def insert_into_players(player_name: str, active_players: list) -> str:
        # Get the id of a player by full_name:
        player_id = get_player_id(player_name, active_players)

        # Get the career stats from the player id and create pandas datafram:
        player = playercareerstats.PlayerCareerStats(player_id=f'{player_id}')
        df = player.get_data_frames()[0]
        df = df.astype(object)

        columns = ', '.join(df.columns) # columns separated by comma
        vals = ', '.join(['%s'] * len(df.columns)) # '%s' separated by cols * total cols

        row_list = df.iloc[0].tolist()     # get the first fow of data
        data = tuple(row_list) 

        # https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
        insert = ( # create insert statement:
        	f'insert into nba.Players ({columns}) '
        	f'values {data};'
        )
        return insert

    # create a list of fav players:
    players = ['Stephen Curry', 'LeBron James', 'Kyrie Irving', 'Kevin Durant', 'Damian Lillard']
    for player in players:
       cursor.execute(insert_into_players(player, active_players)) # execute insert statement

    conn.commit()

if __name__ == "__main__":
    main()
