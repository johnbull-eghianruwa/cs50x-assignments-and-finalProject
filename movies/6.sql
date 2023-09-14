-- query to determine the average rating of all movies released in 2012
SELECT AVG(rating) FROM movies
join ratings on movies_id = ratings.movies_id
WHERE year = 2012;