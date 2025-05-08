def nba_seasons(cursor):
	# Generate season IDs from 1996-97 to 2024-25 (ChatGpt)
	for start_year in range(1996, 2025):
		end_year_short = str(start_year + 1)[-2:]  # get last two digits
		season_id = f"{start_year}-{end_year_short}"

		cursor.execute(
			'insert into nba.Seasons (season_id, start_year, end_year) values (%s, %s, %s);',
			(season_id, start_year, start_year + 1)
		)	

	return cursor
