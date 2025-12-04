from database.models.models import Movie

class MovieRepository:
    def __init__(self, session):
        self.session = session

    def get_all_movies(self):
        movies_list = self.session.query(Movie).all()
        return movies_list

    def get_movie(self, movie_id):
        movie = self.session.query(Movie).filter(Movie.movieId == movie_id).first()
        return movie