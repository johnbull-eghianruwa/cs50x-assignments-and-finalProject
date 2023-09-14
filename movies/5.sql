-- List the titles and release years of all Harry Potter movies, in chronological order
SELECT title(movie) FROM movies
WHERE year like 'Harry Potter%'
ORDER BY year ASC