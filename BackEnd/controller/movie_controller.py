from repository.movie_repository import MovieRepository

class MovieController:
    def __init__(self, movie_repository : MovieRepository):
        self.__repository = movie_repository

    def get_all_movies(self):
        return self.__repository.get_all_movies()

    def get_movie(self, movie_id):
        movie = self.__repository.get_movie(movie_id)
        if movie is not None:
            return {"id": movie.movieId, "title": movie.title}, 200
        else:
            return {"error" : "Movie not found"}, 400