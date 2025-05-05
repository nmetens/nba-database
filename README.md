# nba-database
Author: Nathan Metens
Instructor: Esme Basnet

# Introduction

    I want to build a database about National Basketball Association (NBA) data. More specifically, 
I want to keep track of my favorite players, their statistics, teams, and awards. There are many 
NBA athletes that I like to watch: Steph Curry, LeBron James, Damian Lillard, Luka Doncic, Jimmy 
Butler, Anthony Edwards, and so on. I always go to NBA.com to see the latest NBA games, and 
how many points a player scored, how many 3-pointers they made, and other fun stats. I also 
like to go back in history and watch older players like Michael Jordan, Kobe Bryant, and Tracy McGrady. 
Seeing stats from varying moments in history gives me an idea of who the best players were and what 
they did. This is entertaining to me. There is no shortage of sports data.
    Some valuable information I look at is player age, points per game, and how many MVP or Championship 
trophies they have. I sometimes check the 3-point and free-throw percentage. I love accolades and 
good performances because they make my heart beat faster. Creating a database with my favorite players 
and data will give me lots of practice and easily accessible information I can update and reference in the future.

## 20 Questions to be ansered by the database

1) How many points per game did Lebron James score in his rookie season?
2) What was the average free-throw percentage of each player in the database in 2021?
3) How long has LeBron James been in the NBA?
4) What year was Steph Curry's highest scoring season?
5) How many teams has LeBron James played for in his career? What are they?
6) How many 50-40-90 seasons did Steph Curry have? Steve Kerr? Steve Nash?
7) Who are the top 5 scorers in NBA history, ranked from most to least points?
8) What is the order of players who have the most championships?
9) How many seasons did Steph Curry score more than 25 points per game?
10) How many 50+ point games does Michael Jordan have in his career compared to LeBron James and Kobe Bryant?
11) Who was the youngest player to win the MVP award?
12) Who was the oldest player to win the MVP award?
13) How many NBA players played for 5 or more teams in their careers? What were the teams?
14) Who are the players who won the finals MVP, and what were their stats in the finals?
15) On average, how many seasons does it take for a player to win a championship?
16) What is the average age of a regular-season MVP, and what were their stats?
17) What is the worst regular season record, and what were the stats for that team?
18) What was the best regular season record, and what were the stats?
19) How many more 30 PPG seasons does Michael Jordan have over LeBron James?
20) What was the season with the lowest PPG and still won MVP?

# Resources:

    For creating this database, I plan on using [this website](https://www.basketball-reference.com). 
This website has all of the NBA data from each year in the history of the NBA in easy to use format. 
I’ll have access tables that can be turned into csv files. This will make it simple to transfer the 
data into tables in the database.
    I also will be using a Python module called nba_api which uses all the data from NBA.com at 
endpoints on the web that are accessible via Python and store the data into JSON format. The documentation 
for this module is found on [GitHub and is open source](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md). 
This way, I’ll be able to practice data science in Python and also manage my database using PostgreSQL. 
I’m excited to learn and get started with my database.

## List of Sources

- For creating this database, I plan on using the [basketball-reference](https://www.basketball-reference.com) site
- More NBA data through the [nba_api](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md)
- [env variables](https://developer.vonage.com/en/blog/python-environment-variables-a-primer)
- [virtual environment](https://python.land/virtual-environments/virtualenv)
- [Postresql Docs](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- Postresql Python Library [Psycopg](https://www.psycopg.org/docs/)
- [Port for signing into the PSU database](https://www.postgresql.org/docs/current/runtime-config-connection.html)

# Tutorials

- To create env variables and display:
    `export variable_name="{your_value}"`
    `echo $variable_name`

- To Set up the virtual environment: 
    `python3 -m venv myvenv`
    `source myvenv/bin/activate`
    `deactivate`
