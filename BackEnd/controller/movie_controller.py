from repository.movie_repository import MovieRepository


class MovieController:
    def __init__(self, movie_repository : MovieRepository):
        self.__repository = movie_repository

    def get_all_movies(self):
        list_movies = self.__repository.get_all_movies()
        return {
            "movies": [
                self._serialize_movie(m) 
                for m in list_movies[:50]
            ]}
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
            "genre": [g.genre_name for g in movie.genres]
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
