from repository.movie_repository import MovieRepository

class MovieController:
    def __init__(self, movie_repository : MovieRepository):
        self.__repository = movie_repository

    def get_all_movies(self):
        list_movies = self.__repository.get_all_movies()
        return {"movies": [{"id": m.movie_id, "title": m.title, "genre": [ g.genre_name for g in m.genres]} for m in list_movies[:50]]}

    def get_movie(self, movie_id):
        movie = self.__repository.get_movie(movie_id)
        if movie is not None:
            return {"id": movie.movie_id, "title": movie.title}, 200
        else:
            return {"error" : "Movie not found"}, 400