from database.models.models import Genre

class GenreRepository:

    def __init__(self, session):
        self.session = session

    def get_all_genres(self):
        return self.session.query(Genre).all()