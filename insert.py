import pandas as pd

#def insert_into_player(
# Get the id of a player by full_name:
id_steph_curry =  get_player_id('Stephen Curry', active_players)

# Get the career stats from the player id and create pandas datafram:
steph_curry = playercareerstats.PlayerCareerStats(player_id=f'{id_steph_curry}')
df = steph_curry.get_data_frames()[0]
df = df.astype(object)

columns = ', '.join(df.columns) # columns separated by comma
vals = ', '.join(['%s'] * len(df.columns)) # '%s' separated by cols * total cols

row_list = df.iloc[0].tolist()     # get the first fow of data
data = tuple(row_list) 

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
insert = ( # create insert statement:
	f'insert into nba.Player ({columns}) '
	f'values {data};'
)

cursor.execute(insert) # execute insert statement
