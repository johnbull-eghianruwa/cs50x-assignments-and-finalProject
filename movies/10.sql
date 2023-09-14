SELECT DISTINCT name FROM people
JOIN directors ON directors.person_id = people.id
JOIN movies ON movies.id = directors.movies_id
JOIN rating ON ratings.movie_id = movies.id
WHERE rating >= 9.0;