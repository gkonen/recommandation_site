CREATE MATERIALIZED VIEW movie_tag_occurrence AS
WITH tag_count AS (
	SELECT movie.movie_id, TRIM(LOWER(tag.tag)) as clean_tag, count(*) as occurence FROM movie
	JOIN tag ON movie.movie_id = tag.movie_id
	GROUP BY (movie.movie_id, clean_tag)
), ranked_tag AS (
	SELECT movie_id, clean_tag, occurence,
		ROW_NUMBER() OVER ( PARTITION BY movie_id ORDER BY occurence DESC) as tag_rank
	FROM tag_count
)
SELECT movie_id, clean_tag
FROM ranked_tag
WHERE tag_Rank <=5
WITH DATA