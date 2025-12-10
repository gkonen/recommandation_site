from repository.genre_repository import GenreRepository

class GenreController:
    def __init__(self, genre_repository : GenreRepository):
        self.__repository = genre_repository

    def get_all_genres(self):
        genres = self.__repository.get_all_genres()
        list_genre = [ genre.genre_name for genre in genres]
        return { "genres" : list_genre }