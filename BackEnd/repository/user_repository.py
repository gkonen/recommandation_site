from database.models.models import AppUser, Rating, Tag
from sqlalchemy.orm import joinedload


class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_all_users(self):
        return self.session.query(AppUser).all()

    def get_user(self, user_id):
        return self.session.query(AppUser).filter(AppUser.user_id == user_id).first()
    
    def get_user_by_username(self, username):
        """
        Get a user by username for authentication.
        
        Args:
            username: The username to search for
            
        Returns:
            AppUser object or None
        """
        return self.session.query(AppUser).filter(AppUser.username == username).first()
    
    def get_ratings_by_user(self, user_id):
        """
        Get all ratings by a specific user.
        
        Returns:
            List of Rating objects (empty list if user has no ratings)
        """
        ratings = (
            self.session.query(Rating)
            .options(joinedload(Rating.movie))  # Load all movie data in a single query
            .filter(Rating.user_id == user_id)
            .all()
        )
        return ratings
    
    def get_tags_by_user(self, user_id):
        """
        Get all tags by a specific user.
        
        Returns:
            List of Tag objects (empty list if user has no tags)
        """
        tags = (
            self.session.query(Tag)
            .options(joinedload(Tag.movie))  # Load all movie data in a single query
            .filter(Tag.user_id == user_id)
            .all()
        )
        return tags
    
    def create_user(self, username, password):
        """Create a new user"""
        new_user = AppUser(username=username, pw=password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def get_highly_rated_movies_by_user(self, user_id, min_rating=6, limit=5):
        """
        Get movies that the user rated >= min_rating.
        
        Args:
            user_id: The user's ID
            min_rating: Minimum rating threshold (default: 6)
            limit: Maximum number of movies to return (default: 5)
            
        Returns:
            List of movie_ids ordered by user's rating descending
        """
        from database.models.models import Rating
        
        high_ratings = (
            self.session.query(Rating.movie_id)
            .filter(Rating.user_id == user_id)
            .filter(Rating.rating >= min_rating)
            .order_by(Rating.rating.desc())
            .limit(limit)
            .all()
        )
        
        movie_ids = [rating.movie_id for rating in high_ratings]
        return movie_ids