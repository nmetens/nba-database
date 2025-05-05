-- Create the players table: --
create schema if not exists nba;

drop table if exists nba.Player;
create table if not exists
nba.Player (
	player_id serial primary key,
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
