
from nba_api.stats.endpoints import TeamDetails# Team

team = TeamDetails(team_id=1610612744)
df = team.get_data_frames()[0]
df = df.astype(object)

columns = ', '.join(df.columns)
row_list = df.iloc[0].tolist()
data = tuple(row_list)

print(columns)
print(data)
