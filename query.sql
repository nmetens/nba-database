-- Select all rows from all the tables:
select * from nba.PlayerInfo;
select * from nba.Teams;
select * from nba.Awards;
select * from nba.Seasons;
select * from nba.PlayersStats;
select * from nba.PlayerGameLogs;

-- Create Views for each table that
-- holds the count of all rows:
create view playersstats_count as
select count(*) from nba.playersstats;

create view teams_count as
select count(*) from nba.teams;

create view awards_count as
select count(*) from nba.awards;

create view seasons_count as
select count(*) from nba.seasons;

create view playerinfo_count as
select count(*) from nba.playerinfo;

create view playergamelogs_count as
select count(*) from nba.PlayerGameLogs;

-- Counting all rows from the tables in the nba schema
-- and adding them together to get a total count:
select 
	(select * from playergamelogs_count) + 
	(select * from teams_count) + 
	(select * from awards_count) + 
	(select * from seasons_count) + 
	(select * from playerinfo_count) +
	(select * from playergamelogs_count);

-- Add a full_name column to the table:
ALTER TABLE nba.playersstats 
ADD COLUMN full_name VARCHAR(30);

-- Update the full_name column to be the 
-- first and last name from the playerinfo
-- table:
UPDATE nba.playersstats ps
SET full_name = i.first_name || ' ' || i.last_name
FROM nba.playerinfo i
WHERE i.person_id = ps.player_id;

-- Get the stats for each year in 
-- Stephen Curry's career:
select * from nba.playersstats
where full_name = 'Stephen Curry';

-- Add a ppg column in the stats
-- table that averages the total
-- points per game for each player in 
-- their carreers:
alter table nba.playersstats
add column ppg numeric;

/*alter table nba.playersstats 
drop column ppg cascade;*/

-- Calculate the ppg by dividing
-- the total points in that season
-- by the total games played in that season:
update nba.playersstats
set ppg = round(pts::numeric / gp, 2); -- avoid division by 0

-- Creating a view to keep track
-- of most important stats:
drop view basic_stats;
create view basic_stats as
select
	season_id,
	full_name as "Name",
	ppg as "PPG",
	round(ast::numeric / gp, 2) as "APG",
	round(reb::numeric / gp, 2) as "RPG",
	round(stl::numeric / gp, 2) as "SPG",
	round(blk::numeric / gp, 2) as "BPG"
from
	nba.playersstats;

select * from basic_stats;
select count(*) from basic_stats;
select "Name", "PPG" from basic_stats;

-- Query the View to see who
-- has the most ppg in their career
-- for one single season:
SELECT "Name", "PPG"
FROM basic_stats
ORDER BY "PPG" DESC
LIMIT 1;

-- Select the name of the player who
-- has the most ppg for a single season:
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

-- Select the player with the
-- lowest ppg in a single season
select "Name", min("PPG") from basic_stats
where "PPG" = (
	select min("PPG")
	from basic_stats
)
group by "Name";

-- Select all player names and ppg
-- who had are greater than 15 ppg:
select "Name", "PPG", season_id from  basic_stats
where "PPG" > 15;

-- Create a view to see all important
-- player info, disregarding stats.
drop view player_info;
create or replace view player_info as
select distinct on (p.player_id)
	p.full_name,
	p.player_age,
	i.draft_year,
	i.height,
	i.weight,
	i.birthdate,
	i.school,
	i.jersey,
	i.position,
	i.team_name,
	i.season_exp
from nba.playersstats as p
join nba.playerinfo as i
on p.player_id = i.person_id
order by p.player_id, p.season_id desc;

select * from player_info;

-- See all players who have 15 year of experience or more:
select full_name, birthdate, season_exp from player_info
where season_exp >= 15;

-- Select players with experience levels less than 10 years:
select full_name, season_exp from player_info
where season_exp < 10;

-- Select players who weight less than 200 lbs:
select full_name, weight, height
from player_info
where weight < 200;

-- Calculate player BMI: (ChatGPT BMI)
-- feet to m: (1/0.3048)
-- lbs to kg: (1/0.453592)
-- BMI = weight (kg) / [height (m)]²
-- BMI = (weight/0.453592) / sqrt(height/0.453592)
-- BMI = weight (lb) / height² (in) * 703 
select
  full_name,
  weight,
  height,
  round(weight / power(
    (SPLIT_PART(height, '-', 1)::INT * 12 + SPLIT_PART(height, '-', 2)::INT), 2
  ) * 703) AS "BMI" -- ChatGPT generated equation.
FROM
  player_info;
