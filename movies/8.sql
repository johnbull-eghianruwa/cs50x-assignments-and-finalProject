-- list the names of all people who starred in Toy Story
SELECT name FROM people
JOIN stars.person_id = people.id
JOIN movies ON movies.id = stars.movies_id
WHERE movies.title = "Toy Story";