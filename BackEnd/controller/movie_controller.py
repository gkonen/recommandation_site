from repository.movie_repository import MovieRepository


class MovieController:
    def __init__(self, movie_repository : MovieRepository):
        self.__repository = movie_repository

    def get_all_movies(self, title=None, year=None, genre_name=None):
        """
        Get all movies with optional filters.
        
        Args:
            title: Optional string for filtering by movie title (partial match, case-insensitive)
            year: Optional integer for filtering by release year
            genre_name: Optional string for filtering by genre name
            
        Returns:
            Dictionary containing list of serialized movies
        """
        list_movies = self.__repository.filter_movies(
            title=title,
            year=year,
            genre_name=genre_name
        )
        
        return {
            "movies": [
                self._serialize_movie(m) 
                for m in list_movies[:50]
            ]
        }
        # return {"movies": [{"id": m.movie_id, "title": m.title, "genre": [ g.genre_name for g in m.genres]} for m in list_movies[:50]]}

    def get_movie(self, movie_id):
        movie = self.__repository.get_movie(movie_id)
        if movie is not None:
            return self._serialize_movie(movie), 200
        else:
            return {"error" : "Movie not found"}, 400
        
    def _serialize_movie(self, movie):
        return {
            "id": movie.movie_id,
            "title": movie.title,
            "year": movie.year,
            "genres": [g.genre_name for g in movie.genres]
        }

    # # Replace function above with function below IF we want flexibility to optionally include/exclude fields
    # def _serialize_movie(self, movie, include_genres=True, include_year=True):

    #     result = {
    #         "id": movie.movie_id,
    #         "title": movie.title
    #     }
        
    #     if include_year:
    #         result["year"] = movie.year
        
    #     if include_genres:
    #         result["genre"] = [g.genre_name for g in movie.genres]
        
    #     return result
