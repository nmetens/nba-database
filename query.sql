
-- Selecting all data from each table:
select * from nba.Players;
select * from nba.Teams;
select * from nba.Awards;
select * from nba.Seasons;
select * from nba.CommonPlayerInfo;
select * from nba.PlayerGameLogs;

-- Selecting the total rows for each table:
select count(*) from nba.players;
select count(*) from nba.teams;
select count(*) from nba.awards;
select count(*) from nba.seasons;
select count(*) from nba.commonplayerinfo c;
select count(*) from nba.PlayerGameLogs;

-- Getting all the data for a player:
select * from nba.players
where full_name = 'Stephen Curry';

-- Get the most points per game from the players table:
select max(ppg), full_name from nba.players
group by full_name;

-- Drop and create a new view:
drop view basic_stats;

-- The view selects the basic stats that I am 
-- interested in for my favorite players:
-- (points per game,  assists per game, rebounds
-- per game, etc.):
create view basic_stats as
select
	full_name as "Name",
	ppg as "PPG",
	(ast / gp) as "APG",
	(reb / gp) as "RPG",
	(stl / gp) as "SPG",
	(blk / gp) as "BPG"
from
	nba.players;

-- Quering the view:
select * from basic_stats;
select count(*) from basic_stats;
select "Name", "PPG" from basic_stats;
select max("PPG") from basic_stats;

-- Get the name of the player with 
-- the highest points per game:
select
	"Name"
from
	basic_stats
where
	"PPG" = (
	select
		max("PPG")
	from
		basic_stats
	);

-- Get the player with the lowest
-- points per game in the view:
select "Name" from basic_stats
where "PPG" = (
	select min("PPG")
	from basic_stats
);

-- Get all players PPG that are greater
-- than 15:
select "Name", "PPG" from  basic_stats
where "PPG" > 15;

-- View that holds all important player info:
drop view player_info;
create view player_info as
select
	p.full_name,
	p.player_age as "Draft Age",
	i.height,
	i.weight,
	i.birthdate,
	i.jersey,
	i.position,
	i.last_affiliation,
	i.team_name,
	i.season_exp
from
	nba.players as p
join nba.commonplayerinfo as i
on
	p.player_id = i.person_id;

select * from player_info;

select full_name, season_exp from player_info
where season_exp > 10;

select full_name, season_exp from player_info
where season_exp < 10;

select full_name, weight, height
from player_info
where weight < 200;

-- Calculate player BMI:
-- feet to m: (1/0.3048)
-- lbs to kg: (1/0.453592)
-- BMI = weight (kg) / [height (m)]²
-- BMI = (weight/0.453592) / sqrt(height/0.453592)
-- BMI = weight (lb) / height² (in) * 703 

select
	full_name,
	weight,
	height,
	round(weight / power(height, 2) * 703 ) as "BMI"
from
	player_info;

SELECT
  full_name,
  weight,
  height,
  ROUND(weight / POWER(
    (SPLIT_PART(height, '-', 1)::INT * 12 + SPLIT_PART(height, '-', 2)::INT), 2
  ) * 703) AS "BMI" -- ChatGPT generated equation.
FROM
  player_info;
