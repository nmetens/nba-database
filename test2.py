from nba_api.stats.endpoints import PlayerGameLog, CommonPlayerInfo, TeamGameLog, LeagueGameFinder
import insert as i
import nba_api.stats.static.players as p # Player list

nba_players = p.get_players() # Get all the NBA players

steph_id = i.get_player_id('Stephen Curry')
gamelog = PlayerGameLog(player_id=steph_id, season='2024-25')
df = gamelog.get_data_frames()[0]
print(df.columns)

steph_info = CommonPlayerInfo(player_id=steph_id)
df = steph_info.get_data_frames()[0]
print(df.columns)

#TeamGameLog(team_id=...)

#LeagueGameFinder()
