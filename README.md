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

This graduate student project is for the Intro to Database class at Portland State.

## 24 Questions answered by the database

1) What is the average free-throw percentage of each player in the database in 2021?
2) What year was Steph Curry's highest scoring season?
3) How many teams has LeBron James played for in his career? What are they?
4) Who had 50-40-90 seasons? 
5) Who are the top 5 scorers in the database?
	- Highest scoring points in a regular season game.
	- Create a view to hold the player_id, name, game date, and total points for that game.
6) Create a view that shows each player's points for each game, their age on that game, and the date for that game.
7) What is the order of players who have the most championships?
8) How many seasons did Steph Curry score more than 25 points per game? Changed query to include more players: LeBron, KD, Kyrie?
9) How many points does Steph Curry have throughout his career? How many 3-pointers were made?
10) How many 50+ point games does LeBron James have in his career compared to Stephen Curry?
	- Count the 50-point games for each player in the list of 50+ points.
11) Who was the youngest player to win the MVP award?
12) Who was the oldest player to win the MVP award?
13) How many NBA players played for 5 or more teams in their careers? What were the teams?
14) How many points per game did Lebron James score in the 2010-11 season?
15) On average, how many seasons does it take for a player to win a championship?
15) What is the average age of a player when they win a championship?
16) How long has LeBron James been in the NBA?
	- How many minutes has he played?
	- How many total points?
	- What is career PPG?
	- Calculate the total points given the total seasons and the average career PPG.
17) What was the best regular season record, and what were the stats?
18) What is the worst regular-season record, and what were the stats for that team?
19) Which team has the most MVPS? And who is the head Coach?
20) How many more 30 PPG seasons does James Harden have over Stephen Curry?
21) What was the season with the lowest PPG and still won MVP? What about the highest?
	- And what was the record and age of the player?
22) Which coach has the highest winning percentage in 2024-25?
23) Who are the 2023-24 MVPs' home ppg vs away ppg?

## Updates

Throughout this project, I added dozens of views to the SQL. I played with indexes to speed
up query execution. And I put all of my observations and answers to the questions in the 
[Deliverable 3 PDF](https://github.com/nmetens/nba-database/blob/main/Deliverable%203%20Questions%20to%20Queries%20on%20the%20NBA%20Database.pdf). I used the nba_api to extract rows of data from my favorite players, 
added them to tables through Python functions I created, and then performed many queries 
that joined multiple tables to answer each question. Some questions needed to change
because the nba_api doesn't have any data before the 2008-09 NBA season. I also had so much fun
that I added some extra questions because I was curious about the results.

## Conclusion

I learned a ton in this project. I had fun because I chose a topic of interest and was able to 
dive deeper into the backend instead of using the front end on nba.com. I learned how to connect
API calls to Python, and with the psycopg2 module, I was able to connect Python to SQL.

My final overview and presentation slide for this project are in the [NBA Statistics.pdf](https://github.com/nmetens/nba-database/blob/main/NBA%20Statistics.pdf).

# Resources:

For this project, I used a Python module called nba_api, which uses all the data from NBA.com at 
endpoints on the web that are accessible via Python and stores the data in JSON format. The documentation 
for this module is found on [GitHub and is open source](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md). 
I used data science in Python and also managed my database using PostgreSQL. 

## List of Sources

- More NBA data through the [nba_api](https://github.com/swar/nba_api/blob/master/docs/nba_api/stats/static/players.md)
- [env variables](https://developer.vonage.com/en/blog/python-environment-variables-a-primer)
- [virtual environment](https://python.land/virtual-environments/virtualenv)
- [PostgreSQL Docs](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- PostgreSQL Python Library [Psycopg](https://www.psycopg.org/docs/)
- [Port for signing into the PSU database](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- [Looping through file](https://docs.python.org/3/tutorial/inputoutput.html#methods-of-file-objects)
- [Cursor for db queries](https://www.freecodecamp.org/news/postgresql-in-python/)
- [Insert Formatting](https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html)
- [Pandas Dataframe Documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)

# Tutorials

- To create env variables and display:
    `export variable_name="{your_value}"`
    `echo $variable_name`

- To set up the virtual environment: 
    `python3 -m venv myvenv`
    `source myvenv/bin/activate`
    `deactivate`
