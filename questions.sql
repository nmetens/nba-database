/* Answering the 20 question on the nba data base: */

-- How many points per game did Lebron James score in the 2010-11 season?
-- Changed question because the api has no data for the 2003 nba season
-- which was LeBron James's rookie season.
select s.season_id, full_name, player_age, gp, fgm, fga, ppg
from nba.seasons s 
join nba.playersstats p 
on s.season_id = p.season_id
join nba.playerinfo as i
on p.player_id = i.person_id
where s.season_id = '2010-11' and full_name = 'LeBron James';

-- What was the average free-throw percentage of each player in the database in 2021?
select s.start_year, p.full_name, p.fta, p.ftm, p.ft_pct 
from nba.seasons s
join nba.playersstats p 
on s.season_id = p.season_id
where s.season_id = '2021-22'
order by p.ft_pct desc;

-- How long has LeBron James been in the NBA?

-- What year was Steph Curry's highest scoring season?
select first_name || ' ' || last_name as full_name, s.season_id, gp, ppg 
from nba.seasons s 
join nba.playersstats p 
on s.season_id = p.season_id
join nba.playerinfo p2 
on p.player_id = p2.person_id
where full_name = 'Stephen Curry'
order by ppg desc
limit 1;

-- How many teams has LeBron James played for in his career? What are they?
select season_id, s.full_name, t.abbreviation, count(t.abbreviation)
from nba.playersstats s
join nba.playerinfo p 
on s.player_id = p.person_id
join nba.teams t 
on s.team_id = t.team_id
where p.first_name = 'LeBron'
group by season_id, s.full_name, t.abbreviation;

-- Who had 50-40-90 seasons? Kevin Durant? Klay Thompson?
-- Changed to query active players instead of players who played in 
-- the era when the nba_api didn't have the data:
select s.season_id as "Season", s.player_age, t.abbreviation as "Team", s.full_name, s.ppg, s.fg_pct, s.fg3_pct, s.ft_pct  
from nba.playersstats s
join nba.teams t 
on s.team_abbreviation = t.abbreviation
where s.fg_pct >= 0.5 and s.fg3_pct >= 0.4 and s.ft_pct >= 0.9;

-- Who are the top 5 scorers in RECENT NBA history, ranked from most to least points?
-- Changed to the top 5 scorers in the data in the database instead of all of
-- nba history:
select distinct(p2.full_name), l.game_date, l.matchup, l.wl, l.min, l.reb, l.stl, l.ast, l.pts
from nba.playergamelogs l
join nba.playerinfo p 
on l.player_id = p.person_id
left join nba.playersstats p2 
on p.person_id = p2.player_id
order by pts desc
limit 5;

select l.player_id, p2.full_name, l.game_date, l.matchup, l.wl, l.min, l.reb, l.stl, l.ast, l.pts
from nba.playergamelogs l
join nba.playerinfo p 
  on l.player_id = p.person_id
left join nba.playersstats p2 
  on p.person_id = p2.player_id
where (l.player_id, l.pts) in (
    select player_id, max(pts)
    from nba.playergamelogs
    group by player_id
)
order by l.pts desc
limit 5;

create view points as
select l.player_id, p2.full_name, l.game_date, l.pts
from nba.playergamelogs l
join nba.playerinfo p 
on l.player_id = p.person_id
join nba.playersstats p2 
on p.person_id = p2.player_id;

select * from points;

from nba.playersstats p 
left join nba.playergamelogs l
on l.player_id = l.player_id
order by l.pts desc;

select * 
from nba.playergamelogs p
join nba.playerinfo p2 
on p.player_id = p2.person_id
order by pts desc;

-- What is the order of players who have the most championships?
select distinct ps.full_name 
from nba.playersstats ps;

drop view if exists nba_champions;
create view nba_champions as
select distinct ps.full_name, a.description, a.season
from nba.playersstats ps
join nba.playerinfo p 
on ps.player_id = p.person_id
join nba.awards a 
on p.person_id = a.person_id
where a.description = 'NBA Champion';

select full_name, description as award, season from nba_champions;

select full_name, count(description) as championships
from nba_champions
group by full_name
order by championships desc;

-- How many seasons did Steph Curry score more than 25 points per game?
-- Changed query to include more players: LeBron, KD, Kyrie
select p.full_name, count(*) as high_scoring_season 
from nba.playersstats p
where (p.full_name = 'Stephen Curry' or 
		p.full_name = 'LeBron James' or 
		p.full_name = 'Kevin Durant' or
		p.full_name = 'Kyrie Irving') and p.ppg > 25
group by p.full_name
order by high_scoring_season desc;

-- Added a question: How many points does Steph curry have throughout his career?
-- How many 3pm?

select * from nba.playergamelogs p;

create view points_per_season_curry as
select 
  season_id,
  count(*) as games_played,
  sum(pts) as total_points
from nba.playergamelogs
join nba.playerinfo p 
on player_id = p.person_id
where p.first_name || ' ' || p.last_name = 'Stephen Curry'
group by season_id
order by season_id;

select sum(total_points) as total_career_points from points_per_season_curry;

-- How many 50+ point games does Michael Jordan have in his career compared to LeBron James and Kobe Bryant?
-- Remake question because my database doesn't have any data for Michael Jordan or Kobe Bryant.
-- Instead, search database for Kevin Durant, Damian Lillard, James Harden, and Stephen Curry.

-- There are 139 total games in the database where a player scores at least 50 points:
select count(*) 
from nba.playergamelogs p
where pts >= 50; -- 139

-- Create a view about the stats of all players with 50 plus point games:
create view stats_50_plus as
select
	season_id,
	p2.first_name || ' ' || p2.last_name as "Player Name",
	game_date,
	matchup,
	wl,
	min as "Minutes",
	reb,
	ast,
	stl,
	tov,
	pts as "Points",
	plus_minus as "+/-"
from
	nba.playergamelogs p
join nba.playerinfo p2 
on
	p.player_id = p2.person_id
where 
	p.pts >= 50
;

select * from stats_50_plus;

-- Count the 50 point games for each player in the list of 50+ points...
select "Player Name", count(*) as "50 Point Games"
from stats_50_plus
group by "Player Name"
order by "50 Point Games" desc
limit 10;

-- Who was the youngest player to win the MVP award?
drop view if exists mvp_awards;
create view mvp_awards as
select
	p.first_name || ' ' || p.last_name as "Player Name",
	a.team,
	a.description as "MVP",
	a.season
from
	nba.playerinfo p
join nba.awards a
on
	p.person_id = a.person_id
where
	a.description = 'NBA Most Valuable Player';

select "Player Name", count(*) as "MVPs"
from mvp_awards ma
group by "Player Name";

-- Derrick Rose is not in my database, although he is the youngest player to win MVP.
-- I will see what age each player in my database won MVP and see who was the youngest...
create view mvp_age as
select
	p.first_name || ' ' || p.last_name as "Player Name",
	a.team,
	a.description as "MVP",
	a.season,
	p2.player_age
from
	nba.playerinfo p
join nba.awards a
on
	p.person_id = a.person_id
join nba.playersstats p2 
on p.person_id = p2.player_id and p2.season_id = a.season
where
	a.description = 'NBA Most Valuable Player';

-- In this case, there are two players aged 24 who won 
-- an MVP award.
select
	*
from
	mvp_age
where
	player_age = (
	select
		min(player_age)
	from
		mvp_age
);

-- Who was the oldest player to win the MVP award?
-- Same thing as the last question, but max instead of min:
select
	*
from
	mvp_age
where
	player_age = (
	select
		max(player_age)
	from
		mvp_age
);

-- How many NBA players played for 5 or more teams in their careers? What were the teams?

-- LeBron James played for 3 different teams: CLE, LAL, and MIA
select distinct on (team_abbreviation)
	full_name as player,
	season_id,
	team_abbreviation as team,
	player_age as age,
	ppg
from
	nba.playersstats p
where full_name = 'LeBron James';

create view player_teams as
select distinct on (team_abbreviation)
	full_name as player,
	season_id,
	team_abbreviation as team,
	player_age as age,
	ppg
from
	nba.playersstats p;

select
	p2.first_name || ' ' || p2.last_name as name,
	count(distinct p.team_abbreviation) as teams
from
	nba.playersstats p
join nba.playerinfo p2
on p.player_id = p2.person_id
group by name
order by teams desc
limit 10;

-- Who are the players who won the finals MVP, and what were their stats in the finals?


-- On average, how many seasons does it take for a player to win a championship?

-- What is the average age of a regular-season MVP, and what were their stats?
select * from 

-- What is the worst regular season record, and what were the stats for that team?

-- What was the best regular season record, and what were the stats?
create view season_stats as
select season_id, first_name || ' ' || last_name as player, game_date, matchup, wl, pts 
from nba.playergamelogs l
join nba.playerinfo p 
on l.player_id = p.person_id
order by game_date;

select * from season_stats;

SELECT 
    season_id,
    player,
    SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN wl = 'L' THEN 1 ELSE 0 END) AS losses,
    COUNT(*) AS total_games,
    ROUND(SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS win_percentage
FROM season_stats
GROUP BY season_id, player
ORDER BY season_id, player;

-- How many more 30 PPG seasons does Michael Jordan have over LeBron James?

-- What was the season with the lowest PPG and still won MVP?

