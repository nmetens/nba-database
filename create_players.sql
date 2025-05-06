-- Create the players table: --
create schema if not exists nba;

-- drop table if exists nba.Player;
create table if not exists
nba.Player (
	player_id serial primary key, -- Primary Key
	full_name varchar(30),
	age int,
	height varchar(10), -- 6'8"
	weight int, -- 210, 185
	country varchar(30),
	position varchar(5), -- PG, SG, SF, PF, C
	active int, -- true/false
	debut_year date -- Format YYYY-MM-DD
);

insert into nba.Player 
	(full_name, age, height, country, position, active, debut_year)
values
('Stephen Curry', 36, '62', 'USA', 'PG', 1, '2011-10-30');


-- Creatig the Team table: --
create table if not exists
nba.Team (
	team_id serial primary key, -- Primary Key
	name varchar(50),
	abbrev varchar(30),
	city varchar(30),
	coach varchar(30)
);

insert into nba.Team 
	(name, abbrev, city, coach)
values
	('Golden State Warriors', 'GSW', 'San Francisco', 'Steve Kerr');

-- Creating the Season table: --
create table if not exists
nba.Season (
	season_id serial primary key, -- Primary Key
	year_start date,
	year_end date
);

-- Creating the Award table: --
create table if not exists
nba.Award (
	award_id serial primary key, --Primary Key
	name varchar(30),
	description varchar(100)
);

-- Creating them PlayerAward table: --
create table if not exists
nba.PlayerAward (
	player_id int references nba.Player(player_id), -- Foreign Key
	award_id int references nba.Award(award_id), -- Foreign Key
	season_id int references nba.Season(season_id), -- Foreign Key
	primary key (player_id, award_id, season_id) -- Composite Key
);

-- Creating the PlayerTeamSeason table: --
create table if not exists
nba.PlayerTeamSeason (
	player_id int references nba.Player(player_id),
	team_id int references nba.Team(team_id),
	season_id int references nba.Season(season_id),
	jersey_number int,
	primary key (player_id, team_id, season_id)	
);

-- Create the RegularSeasonStats table: --
create table if not exists
nba.RegularSeasonStats (
	stat_id serial primary key,

	player_id int references nba.Player(player_id),
	season_id int references nba.Season(season_id),
	team_id int references nba.Team(team_id),
	
	games_played int,
	minutes_per_game float,
	ppg float, -- points per game
	fgm float, -- field goals (fg) made
	fga float, -- fg attempted
	fgp float, -- fg percentage (%)
	tpm float, -- three pointers (tp) made
	tpa float, -- tp attempted
	tpp float, -- tp %
	ftm float, -- free throws (ft)
	fta float,
	ftp float,
	apg float, -- assists per game
	rpg float, -- rebounds
	spg float, -- steals
	blk float, -- blocks
	tov float, -- turn overs per game
	pm float   -- plus minus score
);

-- Create the PlayoffStats table: --
create table if not exists
nba.PlayoffStats (
	stat_id serial primary key,

	player_id int references nba.Player(player_id),
	season_id int references nba.Season(season_id),
	team_id int references nba.Team(team_id),
	
	games_played int,
	minutes_per_game float,
	ppg float, -- points per game
	fgm float, -- field goals (fg) made
	fga float, -- fg attempted
	fgp float, -- fg percentage (%)
	tpm float, -- three pointers (tp) made
	tpa float, -- tp attempted
	tpp float, -- tp %
	ftm float, -- free throws (ft)
	fta float,
	ftp float,
	apg float, -- assists per game
	rpg float, -- rebounds
	spg float, -- steals
	blk float, -- blocks
	tov float, -- turn overs per game
	pm float   -- plus minus score
);
