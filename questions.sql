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

-- How many 50-40-90 seasons did Steph Curry have? Steve Kerr? Steve Nash?
-- Who are the top 5 scorers in NBA history, ranked from most to least points?
-- What is the order of players who have the most championships?
-- How many seasons did Steph Curry score more than 25 points per game?
-- How many 50+ point games does Michael Jordan have in his career compared to LeBron James and Kobe Bryant?
-- Who was the youngest player to win the MVP award?
-- Who was the oldest player to win the MVP award?
-- How many NBA players played for 5 or more teams in their careers? What were the teams?
-- Who are the players who won the finals MVP, and what were their stats in the finals?
-- On average, how many seasons does it take for a player to win a championship?
-- What is the average age of a regular-season MVP, and what were their stats?
-- What is the worst regular season record, and what were the stats for that team?
-- What was the best regular season record, and what were the stats?
-- How many more 30 PPG seasons does Michael Jordan have over LeBron James?
-- What was the season with the lowest PPG and still won MVP?

