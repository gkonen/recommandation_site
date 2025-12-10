from repository.movie_repository import MovieRepository
import math


class MovieController:
    def __init__(self, movie_repository : MovieRepository):
        self.__repository = movie_repository

    def get_all_movies(self, title=None, year=None, genre_name=None, page=1, per_page=50):
        """
        Get movies with optional filters and pagination.

        Args:
            title: Optional string for filtering by movie title (partial match, case-insensitive)
            year: Optional integer for filtering by release year
            genre_name: Optional string for filtering by genre name
            page: Page number (default 1)
            per_page: Number of results per page (default 50)

        Returns:
            Dictionary containing paginated movies and metadata
        """
        movies, total = self.__repository.filter_movies(
            title=title,
            year=year,
            genre_name=genre_name,
            page=page,
            per_page=per_page
        )

        total_pages = math.ceil(total / per_page) if total > 0 else 0
        serialized_movies = [ self._serialize_movie(m) for m in list_movies[:50] ]

        return {
            "movies": serialized_movies,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": total,
                "total_pages": total_pages,
                "has_prev": page > 1,
                "has_next": page < total_pages
            }
        }
        # return {"movies": [{"id": m.movie_id, "title": m.title, "genre": [ g.genre_name for g in m.genres]} for m in list_movies[:50]]}

    def get_movie(self, movie_id):
        movie = self.__repository.get_movie(movie_id)
        if movie is not None:
            return self._serialize_movie(movie), 200
        else:
            return {"error" : "Movie not found"}, 400

    def _serialize_movie(self, movie):
        score = movie.score.rating
        genre_list = [g.genre_name for g in movie.genres]
        tags = [tag.clean_tag for tag in movie.tags]
        return {
            "id": movie.movie_id,
            "title": movie.title,
            "year": movie.year,
            "score": score,
            "genres": genre_list,
            "tags" : tags
        }
