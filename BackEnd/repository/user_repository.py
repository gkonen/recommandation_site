from database.models.models import AppUser

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