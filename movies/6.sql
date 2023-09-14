-- query to determine the average rating of all movies released in 2012
SELECT AVG(rating) FROM movies
JOIN  ratings on movies_id = ratings.movies_id
WHERE year = 2012;