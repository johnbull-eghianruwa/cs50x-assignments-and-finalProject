-- Where a SQL query that returns the average energy of all the songs that feature other artists

SELCT name FROM songs WHERE name LIKE "%feat.%";
