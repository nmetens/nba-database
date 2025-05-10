create schema NBA;

create table if not exists
NBA.Seasons (
        SEASON_ID varchar(10) primary key, -- e.g. '2024-25'
        START_YEAR int not null, -- 2024
        END_YEAR int not null -- 2025
);

-- Table: Teams
create table if not exists
NBA.Teams (
        TEAM_ID int primary key, -- PK
        ABBREVIATION varchar(10),
        NICKNAME varchar(30),
        YEARFOUNDED int,
        CITY varchar(30),
        ARENA varchar(30),
        ARENACAPACITY int,
        OWNER varchar(50),
        GENERALMANAGER varchar(50),
        HEADCOACH varchar(50),
        DLEAGUEAFFILIATION varchar(50)
);

-- Table: PlayerInfo
create table if not exists
NBA.PlayerInfo (
        PERSON_ID int primary key,
        FIRST_NAME varchar(50),
        LAST_NAME varchar(50),
        DISPLAY_FIRST_LAST varchar(100),
        DISPLAY_LAST_COMMA_FIRST varchar(100),
        DISPLAY_FI_LAST varchar(100),
        PLAYER_SLUG varchar(50),
        BIRTHDATE date,
        SCHOOL varchar(100),
        COUNTRY varchar(50),
        LAST_AFFILIATION varchar(100),
        HEIGHT varchar(10),
        WEIGHT int,
        SEASON_EXP int,
        JERSEY varchar(10),
        POSITION varchar(20),
        ROSTERSTATUS varchar(20),
        GAMES_PLAYED_CURRENT_SEASON_FLAG boolean,
        TEAM_ID int references NBA.Teams(TEAM_ID),
        TEAM_NAME varchar(50),
        TEAM_ABBREVIATION varchar(20),
        TEAM_CODE varchar(20),
        TEAM_CITY varchar(50),
        PLAYERCODE varchar(50),
        FROM_YEAR int,
        TO_YEAR int,
        DLEAGUE_FLAG boolean,
        NBA_FLAG boolean,
        GAMES_PLAYED_FLAG boolean,
        DRAFT_YEAR int,
        DRAFT_ROUND varchar(5),
        DRAFT_NUMBER varchar(5),
        GREATEST_75_FLAG varchar(5)
);

-- Table: Players
create table if not exists
NBA.PlayersStats (
        PLAYER_ID int references NBA.PlayerInfo(PERSON_ID), -- FK
        SEASON_ID varchar(10) references NBA.Seasons(SEASON_ID), -- FK
        LEAGUE_ID int,
        TEAM_ID int references NBA.Teams(TEAM_ID) on delete set null, -- FK
        TEAM_ABBREVIATION varchar(10),
        PLAYER_AGE float,
        GP int,
        GS int,
        MIN float,
        FGM int,
        FGA int,
        FG_PCT float,
        FG3M int,
        FG3A int,
        FG3_PCT float,
        FTM int,
        FTA int,
        FT_PCT float,
        OREB int,
        DREB int,
        REB int,
        AST int,
        STL int,
        BLK int,
        TOV int,
        PF int,
        PTS int,
        primary key (SEASON_ID, PLAYER_ID, TEAM_ID)
);

-- Table: Awards
create table if not exists
NBA.Awards (
        AWARD_ID serial primary key, -- PK
        PERSON_ID int references NBA.PlayerInfo(PERSON_ID) on delete cascade, -- FK
        FIRST_NAME varchar (50),
        LAST_NAME varchar(50),
        TEAM varchar(50),
        DESCRIPTION TEXT,
        ALL_NBA_TEAM_NUMBER int,
        SEASON varchar(20),
        MONTH varchar(20),
        WEEK varchar(20),
        CONFERENCE varchar(20),
        TYPE varchar(50),
        SUBTYPE1 varchar(50),
        SUBTYPE2 varchar(50),
        SUBTYPE3 varchar(50)
);

-- Table: PlayerGameLogs
create table if not exists
NBA.PlayerGameLogs (
        SEASON_ID varchar(10) references NBA.Seasons(season_id),
        PLAYER_ID int references NBA.PlayerInfo(PERSON_ID) on delete cascade,
        GAME_ID varchar(20),
        GAME_DATE date,
        MATCHUP varchar(50),
        WL varchar(2),
        MIN float,
        FGM int,
        FGA int,
        FG_PCT float,
        FG3M int,
        FG3A int,
        FG3_PCT float,
        FTM int,
        FTA int,
        FT_PCT float,
        OREB int,
        DREB int,
        REB int,
        AST int,
        STL int,
        BLK int,
        TOV int,
        PF int,
        PTS int,
        PLUS_MINUS float,
        VIDEO_AVAILABLE int,
        primary key (SEASON_ID, PLAYER_ID, GAME_ID)
);
