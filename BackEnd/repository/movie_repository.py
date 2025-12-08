from database.models.models import Movie
from database.models.models import Genre


class MovieRepository:
    def __init__(self, session):
        self.session = session

    def get_all_movies(self):
        movies_list = self.session.query(Movie).all()
        return movies_list

    def get_movie(self, movie_id):
        movie = self.session.query(Movie).filter(Movie.movie_id == movie_id).first()
        return movie
    
    def filter_movies(self, year=None, genre_name=None):
        """
        Filter movies by year and/or genre.
        
        Args:
            year: Optional integer for filtering by release year
            genre_name: Optional string for filtering by genre name
            
        Returns:
            List of Movie objects matching the filter criteria
        """
        query = self.session.query(Movie)
        
        if year is not None:
            query = query.filter(Movie.year == year)
        
        if genre_name is not None:
            query = query.join(Movie.genres).filter(Genre.genre_name == genre_name)
        
        return query.distinct().all()

    # def delete_movie(self, movie_id):
    #     """
    #     Delete a movie record.
    #     Args:
    #         movie_id: The ID of the movie to delete
    #     Returns:
    #         True if movie was deleted, False if movie not found
    #     """
    #     movie = self.session.query(Movie).filter(Movie.movie_id == movie_id).first()
    #     if movie:
    #         self.session.delete(movie)
    #         self.session.commit()
    #         return True
    #     return False