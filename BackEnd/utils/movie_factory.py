from flask import current_app

from controller.movie_controller import MovieController
from repository.movie_repository import MovieRepository

class MovieFactory:

    @staticmethod
    def get_controller(session):
        movie_repository = MovieRepository(session)
        movie_controller = MovieController(movie_repository, current_app.extensions['recommendation'])
        return movie_controller