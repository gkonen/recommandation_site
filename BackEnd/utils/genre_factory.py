from controller.genre_controller import GenreController
from repository.genre_repository import GenreRepository


class GenreFactory:

    @staticmethod
    def get_controller(session):
        genre_repository = GenreRepository(session)
        genre_controller = GenreController(genre_repository)
        return genre_controller