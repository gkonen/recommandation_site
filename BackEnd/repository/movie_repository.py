from database.models.models import Movie
from database.models.models import Genre


class MovieRepository:
    def __init__(self, session):
        self.session = session

    def get_movie(self, movie_id) -> Movie:
        movie = self.session.query(Movie).filter(Movie.movie_id == movie_id).first()
        return movie
    
    def filter_movies(self, title=None, year=None, genre_name=None) -> list[Movie]:
        """
        Filter movies by title, year and/or genre. If no filters provided, returns all movies.
        
        Args:
            title: Optional string for filtering by movie title (partial match, case-insensitive)
            year: Optional integer for filtering by release year
            genre_name: Optional string for filtering by genre name
            
        Returns:
            List of Movie objects matching the filter criteria
        """
        query = self.session.query(Movie)
        
        if title is not None:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        
        if year is not None:
            query = query.filter(Movie.year == year)
        
        if genre_name is not None:
            query = query.join(Movie.genres).filter(Genre.genre_name.ilike(f"%{genre_name}%"))
        
        return query.distinct().all()