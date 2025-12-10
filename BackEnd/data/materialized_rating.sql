CREATE MATERIALIZED VIEW movie_rating AS
SELECT movie.movie_id, AVG(rating.rating) as score from movie
JOIN rating on movie.movie_id = rating.movie_id
GROUP by movie.movie_id
WITH DATA;