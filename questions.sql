------------------------------
--NBA DATABASE
------------------------------
select * from nba.awards a;
select * from nba.playergamelogs p;

select season_id, count(season_id) from nba.playergamelogs
group by season_id
order by season_id;

select * from nba.playerinfo p;
select * from nba.playersstats p;
select * from nba.seasons s;
select * from nba.teams t;
------------------------------
-- 1) What was the average free-throw percentage of each player in the database in 2021?
select s.start_year, p.full_name, p.fta, p.ftm, p.ft_pct 
from nba.seasons s
join nba.playersstats p 
on s.season_id = p.season_id
where s.season_id = '2021-22'
order by p.ft_pct desc;

-- 2) What year was Steph Curry's highest scoring season?
select first_name || ' ' || last_name as full_name, s.season_id, gp, ppg 
from nba.seasons s 
join nba.playersstats p 
on s.season_id = p.season_id
join nba.playerinfo p2 
on p.player_id = p2.person_id
where full_name = 'Stephen Curry'
order by ppg desc
limit 1;

-- 3) How many teams has LeBron James played for in his career? What are they?
create view lebron_teams as
select distinct t.abbreviation
from nba.playersstats s
join nba.playerinfo p 
on s.player_id = p.person_id
join nba.teams t 
on s.team_id = t.team_id
where p.first_name = 'LeBron';

-- Teams:
select * from lebron_teams;

-- Total teams count:
select count(*) as total_teams 
from lebron_teams;

-- 4) Who had 50-40-90 seasons? Kevin Durant? Klay Thompson?
-- Changed to query active players instead of players who played in 
-- the era when the nba_api didn't have the data:
select s.season_id as "Season", s.player_age, t.abbreviation as "Team", s.full_name, s.ppg, s.fg_pct, s.fg3_pct, s.ft_pct  
from nba.playersstats s
join nba.teams t 
on s.team_abbreviation = t.abbreviation
where s.fg_pct >= 0.5 and s.fg3_pct >= 0.4 and s.ft_pct >= 0.9;

-- 5a) Who are the top 5 scorers in RECENT NBA history, ranked from most to least points?
-- Changed to the top 5 scorers in the data in the database instead of all of
-- nba history:

-- Highest scoring points in a regular season game:
select distinct(p2.full_name), l.game_date, l.matchup, l.wl, l.min, l.reb, l.stl, l.ast, l.pts
from nba.playergamelogs l
join nba.playerinfo p 
on l.player_id = p.person_id
left join nba.playersstats p2 
on p.person_id = p2.player_id
order by pts desc
limit 5;

-- 5b) Create a view to hold the player_id, name, game date, and total points for that game:

drop view if exists season_high;
create view season_high as
select distinct * from points
order by pts desc
limit 100;

select * from season_high;

----------
-- 6) Create a view that shows each player's points for each game, their age on that game,
-- and the date for that game.
create view player_season_high_points as
select p.game_date, p2.first_name || ' ' || p2.last_name as "Player Name", p3.player_age, p.pts 
from nba.playergamelogs p
join nba.playerinfo p2 
on p.player_id = p2.person_id
join nba.playersstats p3 
on p.player_id = p3.player_id and p.season_id = p3.season_id
order by p.pts desc;

-- Show the highest points scored for each player and what age they were.
-- See only the top 10 points records for the regular season:
select distinct * from player_season_high_points
order by pts desc
limit 10;

-- 7) What is the order of players who have the most championships?
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

-- 8) How many seasons did Steph Curry score more than 25 points per game?
-- Changed query to include more players: LeBron, KD, Kyrie
select p.full_name, count(*) as high_scoring_season 
from nba.playersstats p
where (p.full_name = 'Stephen Curry' or 
		p.full_name = 'LeBron James' or 
		p.full_name = 'Kevin Durant' or
		p.full_name = 'Kyrie Irving') and p.ppg > 25
group by p.full_name
order by high_scoring_season desc;

-- 9) Added a question: How many points does Steph curry have throughout his career?
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

-- 10) How many 50+ point games does Michael Jordan have in his career compared to LeBron James and Kobe Bryant?
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

-- 11) Who was the youngest player to win the MVP award?
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

-- 12) Who was the oldest player to win the MVP award?
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

-- 13) How many NBA players played for 5 or more teams in their careers? What were the teams?
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

-- 14) Who are the players who won the finals MVP, and what were their stats in the finals?
-- I have no data regarding the nba playoffs besides brackets from the api.
-- Question changed: 

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

-- 15a) On average, how many seasons does it take for a player to win a championship?
drop view if exists seasons_to_champ;
create view seasons_to_champ as
select distinct on (full_name)
	s.season_id, full_name, team, description, min(player_age) age, s.end_year, draft_year, ppg 
from nba.awards a
join nba.playersstats p 
on a.person_id = p.player_id and a.season = p.season_id
join nba.playerinfo p2 
on p.player_id = p2.person_id
join nba.seasons s 
on p.season_id = s.season_id
where description = 'NBA Champion'
group by full_name, s.season_id, full_name, team, description, end_year, draft_year, ppg;

select * from seasons_to_champ;

select round(avg(end_year - draft_year), 0) as average_seasons_before_champ
from seasons_to_champ;

-- 15b) What is the average age of a player when they win a championship?
select round(sum(age)::numeric / count(*)::numeric, 0) from seasons_to_champ;

-- 16)
-- Extra 1) How long has LeBron James been in the NBA?
create view total_seasons as
select
	count(*) as total_seasons
from
	nba.playersstats p
where full_name = 'LeBron James';

select * from total_seasons;

-- How many minutes has he played?
select
	sum(min) as total_seasons
from
	nba.playersstats p
where full_name = 'LeBron James';

-- How many total points?
create view total_points as
select
	sum(pts) as total_points
from
	nba.playersstats p
where full_name = 'LeBron James';

select * from total_points;

-- What is is career ppg?
create view career_ppg as
select
	round(avg(ppg), 2) as total_seasons
from
	nba.playersstats p
where full_name = 'LeBron James';

select * from career_ppg;

-- Calculate the total points given the total seasons and the avg career ppg:
create view total_points_calc as
select
	round(avg(ppg) * sum(gp), 2) as total_points
from
	nba.playersstats p
where full_name = 'LeBron James';

select * from total_points_calc;

-- 17a) What was the best regular season record, and what were the stats?
create view season_stats as
select season_id, first_name || ' ' || last_name as player, game_date, matchup, wl, pts 
from nba.playergamelogs l
join nba.playerinfo p 
on l.player_id = p.person_id
order by game_date;

select * from season_stats;

create view regular_season_record as
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

select
	season_id,
	player,
	wins,
	losses,
	total_games,
	win_percentage
from
	regular_season_record rsr
where
	wins = (
	select
		max(wins)
	from
		regular_season_record rsr2
);

-- 17b) What is the worst regular season record, and what were the stats for that team?
select -- This is the season that steph curry got injured.
	season_id,
	player,
	wins,
	losses,
	total_games,
	win_percentage
from
	regular_season_record rsr
where
	wins = (
	select
		min(wins)
	from
		regular_season_record rsr2
);

-- 18) Which team has the most MVPS? And who is the head Coach?
create view total_mvps as
select distinct p.season_id, abbreviation, headcoach, full_name, draft_round, draft_number, gp, ppg, description,
	SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN wl = 'L' THEN 1 ELSE 0 END) AS losses,
    ROUND(SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS win_percentage
from nba.teams t 
join nba.playersstats p 
on t.team_id = p.team_id and t.abbreviation = p.team_abbreviation
join nba.playerinfo p2 
on p.player_id = p2.person_id
join nba.awards a 
on p2.person_id = a.person_id and a.season = p.season_id
join nba.playergamelogs p3 
on p2.person_id = p3.player_id and a.season = p3.season_id
where description = 'NBA Most Valuable Player'
group by p.season_id, abbreviation, headcoach, full_name, draft_round, draft_number, gp, ppg, description;

select * from total_mvps;

select distinct abbreviation, headcoach, count(*) as total_mvps 
from total_mvps
group by abbreviation, headcoach
order by total_mvps desc
limit 1;

-- 19) How many more 30 PPG seasons does Michael Jordan have over LeBron James?
-- Changed from Michael Jordan to James Harden...
-- Changed from James Harden to Stphen Curry...
create view high_scoring_seasons as
select * from nba.playersstats
where ppg >= 30;

select * from high_scoring_seasons
where full_name = 'LeBron James';

select season_id, full_name, ppg, pts, gp 
from nba.playersstats p
where full_name = 'LeBron James';
	
drop view if exists player_scoring;
create view player_scoring as
select full_name, count(*) as "30 pt avg seasons" 
from high_scoring_seasons
group by full_name
order by "30 pt avg seasons" desc;

select * from player_scoring;

create view lebron as
select "30 pt avg seasons" 
from player_scoring
where full_name = 'LeBron James';

select * from lebron;

create view steph as
select "30 pt avg seasons" 
from player_scoring
where full_name = 'Stephen Curry';

select * from steph;

-- Joining the two views and answering the question:
SELECT 
  p1."30 pt avg seasons" - p2."30 pt avg seasons" AS difference
FROM 
  player_scoring p1,
  player_scoring p2
WHERE 
  p1.full_name = 'LeBron James'
  AND p2.full_name = 'Stephen Curry';

-- 20) What was the season with the lowest PPG and still won MVP? What about the highes?
-- ADDED: And what was the record, and age of the player...
drop view if exists mvp;
create view mvp as
select
	season,
	person_id,
	first_name || ' ' || last_name as player,
	team,
	description
from
	nba.awards
where description = 'NBA Most Valuable Player'
order by season;

select * from mvp;

create view mvp_stats as
select m.season, m.player, m.team, m.description, p2.player_age, p2.gp, p2.fg3m, p2.ppg
from mvp m 
join nba.playerinfo p 
on m.player = p.display_first_last
join nba.playersstats p2 
on p.person_id = p2.player_id and m.season = p2.season_id;

select * from mvp_stats;

-- Lowest ppg with MVP:
create view small_ppg_mvp as
select * 
from mvp_stats
where ppg = (select min(ppg) from mvp_stats);

select * from small_ppg_mvp;

-- Highest ppg with MVP:
create view big_ppg_mvp as
select * 
from mvp_stats
where ppg = (select max(ppg) from mvp_stats);

select * from big_ppg_mvp;

-- Getting the data for the lowest:
select
	season,
	player,
	team,
	description,
	s.player_age,
	s.ppg,
	SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN wl = 'L' THEN 1 ELSE 0 END) AS losses,
    ROUND(SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS win_percentage
from
	small_ppg_mvp s
join nba.playersstats p 
on
	s.player_age = p.player_age
	and s.player = p.full_name
join nba.seasons s2 
on
	p.season_id = s2.season_id
join nba.playergamelogs p2 
on
	s2.season_id = p2.season_id
	and p.player_id = p2.player_id
group by 
	season,
	player,
	team,
	description,
	s.ppg,
	s.player_age;

-- Get the data for the highest:
select
	season,
	player,
	team,
	description,
	s.player_age,
	s.ppg,
	SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) AS wins,
    SUM(CASE WHEN wl = 'L' THEN 1 ELSE 0 END) AS losses,
    ROUND(SUM(CASE WHEN wl = 'W' THEN 1 ELSE 0 END) * 100.0 / COUNT(*), 2) AS win_percentage
from
	big_ppg_mvp s
join nba.playersstats p 
on
	s.player_age = p.player_age
	and s.player = p.full_name
join nba.seasons s2 
on
	p.season_id = s2.season_id
join nba.playergamelogs p2 
on
	s2.season_id = p2.season_id
	and p.player_id = p2.player_id
group by 
	season,
	player,
	team,
	description,
	s.ppg,
	s.player_age;

-- Extra 1) Which coach has the highest winning percentage in 2024?
drop view if exists wins;

create view wins as
select
	headcoach,
	abbreviation,
	SUM(case when wl = 'W' then 1 else 0 end) as wins,
	SUM(case when wl = 'L' then 1 else 0 end) as losses,
	ROUND(SUM(case when wl = 'W' then 1 else 0 end) * 100.0 / COUNT(*), 2) as win_percentage
from
	nba.playergamelogs p
join nba.seasons s 
on
	p.season_id = s.season_id
join nba.playersstats p2 
on
	s.season_id = p2.season_id
	and p.player_id = p2.player_id
join nba.playerinfo p3 
on
	p2.player_id = p3.person_id
join nba.teams t 
on
	p3.team_id = t.team_id
where
	p.season_id = '2024-25'
group by
	headcoach,
	abbreviation
order by
	win_percentage desc
limit 1;

select headcoach from wins;

-- Extra 2) What is the 2023-24 mvps home ppg vs away ppg?
drop view if exists mvp2023_24;
create view mvp2023_24 as
select
	person_id as player_id
from
	nba.awards a
where
	season = '2023-24'
	and description = 'NBA Most Valuable Player';

select * from mvp2023_24;

create view home_vs_away as
select
	game_date,
	full_name,
	matchup,
	wl,
	p3.pts,
	CASE
	    WHEN matchup ILIKE '%@%' THEN 'Away'
	    WHEN matchup ILIKE '%vs.%' THEN 'Home'
	    ELSE 'Unknown'
  	END AS location
from
	nba.playerinfo p
join nba.playersstats p2 
on
	p.person_id = p2.player_id
join nba.seasons s 
on
	p2.season_id = s.season_id
join nba.playergamelogs p3 
on
	p.person_id = p3.player_id
	and p2.season_id = p3.season_id
where
	p2.player_id = (
	select
		*
	from
		mvp2023_24)
	and p2.season_id = '2023-24';

select * from home_vs_away;

create view home_vs_away_pts as
select 
	count(case when location = 'Away' then 1 end) as away_games,
	sum(case when location = 'Away' then pts end) as away_pts,
	count(case when location = 'Home' then 1 end) as home_games,
	sum(case when location = 'Home' then pts end) as home_pts
from home_vs_away;

select * from home_vs_away_pts;

select 
	round(away_pts/away_games::numeric, 2) as away_ppg,
	round(home_pts/home_games::numeric, 2) as home_ppg
from home_vs_away_pts;
