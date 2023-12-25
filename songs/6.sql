-- Write a SQL  query to list the names of songs that are by post malone

SELECT name FROM songs WHERE artist_id = (SELECT id FROM artists
WHERE name = "Post Malone");
