from database.models.models import AppUser

class UserRepository:
    def __init__(self, session):
        self.session = session

    def get_all_users(self):
        return self.session.query(AppUser).all()

    def get_user(self, user_id):
        return self.session.query(AppUser).filter(AppUser.userId == user_id).first()