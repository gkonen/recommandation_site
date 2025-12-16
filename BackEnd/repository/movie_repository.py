import time
from sqlalchemy.dialects.postgresql import insert
from database.models.models import Movie, Rating
from database.models.models import Genre


class MovieRepository:
    def __init__(self, session):
        self.session = session

    def get_movie(self, movie_id) -> Movie:
        movie = self.session.query(Movie).filter(Movie.movie_id == movie_id).first()
        return movie
    
    def filter_movies(self, title=None, year=None, genre_name=None, page=1, per_page=50) -> tuple[list[Movie], int]:
        """
        Filter movies by title, year and/or genre, with pagination. If no filters provided, returns all movies.
        
        Args:
            title: Optional string for filtering by movie title (partial match, case-insensitive)
            year: Optional integer for filtering by release year
            genre_name: Optional string for filtering by genre name
            page: Page number (starts at 1)
            per_page: Number of results per page

        Returns:
            Tuple of (list of movies, total count)
        """
        query = self.session.query(Movie)
        
        if title is not None:
            query = query.filter(Movie.title.ilike(f"%{title}%"))
        
        if year is not None:
            query = query.filter(Movie.year == year)
        
        if genre_name is not None:
            query = query.join(Movie.genres).filter(Genre.genre_name.ilike(f"%{genre_name}%"))
        
        query = query.distinct()

        # Get total count before pagination
        total = query.count()

        # Apply pagination
        offset = (page - 1) * per_page
        movies = query.offset(offset).limit(per_page).all()

        return movies, total

    def add_rating(self, movie_id, user_id, rating):
        stmt = insert(Rating).values(movie_id=movie_id,
                                     user_id=user_id,
                                     rating=rating,
                                     recorded_at=int(time.time()))
        stmt = stmt.on_conflict_do_update(
            index_elements=["movie_id", "user_id"],
            set_= {
                "rating": stmt.excluded.rating,
                "recorded_at": stmt.excluded.recorded_at
            }
        )
        self.session.execute(stmt)
        self.session.commit()

    def get_top_rated_movies(self, limit=20):
        """
        Get top-rated movies by average score.
        
        Args:
            limit: Number of movies to return
            
        Returns:
            List of Movie objects ordered by score descending
        """
        movies = (
            self.session.query(Movie)
            .filter(Movie.score.isnot(None))  # Only movies with scores
            .order_by(Movie.score.desc())
            .limit(limit)
            .all()
        )
        return movies
    
    def get_movies_by_ids(self, movie_ids):
        """
        Get multiple movies by their IDs in a single query.
        
        Args:
            movie_ids: List of movie IDs
            
        Returns:
            List of Movie objects
        """
        if not movie_ids:
            return []
        
        movies = self.session.query(Movie).filter(Movie.movie_id.in_(movie_ids)).all()
        return movies