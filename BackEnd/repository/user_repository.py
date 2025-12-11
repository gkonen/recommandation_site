from database.models.models import AppUser
from database.models.models import Rating
from database.models.models import Tag


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
    
    def user_exists(self, user_id):
        """
        Check if a user exists in the database.
        
        Returns:
            True if user exists, False otherwise
        """
        user = self.session.query(AppUser).filter(AppUser.user_id == user_id).first()
        return user is not None
    
    def get_ratings_by_user(self, user_id):
        """
        Get all ratings by a specific user.
        
        Returns:
            List of Rating objects (empty list if user has no ratings)
        """
        ratings = self.session.query(Rating).filter(Rating.user_id == user_id).all()
        return ratings
    
    def get_tags_by_user(self, user_id):
        """
        Get all tags by a specific user.
        
        Returns:
            List of Tag objects (empty list if user has no tags)
        """
        tags = self.session.query(Tag).filter(Tag.user_id == user_id).all()
        return tags