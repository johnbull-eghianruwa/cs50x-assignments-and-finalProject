-- Where a SQL query that returns the average energy of all the songs that are by Drake

SELECT AVG(energy) FROM songs
WHERE artist_id = (SELECT id FROM artists WHERE name = "Drake");
