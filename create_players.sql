-- Create the players table: --
create table if not exists
Player (
	player_id serial primary key,
	full_name varchar(30),
	age int,
	height varchar(10), -- 6'8"
	weight int, -- 210, 185
	country varchar(30),
	position varchar(5), -- PG, SG, SF, PF, C
	active boolean, -- true/false
	debut_year date, -- Format YYYY-MM-DD
);
