from repository.user_repository import UserRepository

class UserController:
    def __init__(self, user_repository : UserRepository):
        self.__repository = user_repository

    def get_all_users(self):
        return self.__repository.get_all_users()

    def get_user(self, user_id):
        user = self.__repository.get_user(user_id)
        if user is not None:
            return {"id": user.userId, "username": user.username}, 200
        else:
            return {"error" : "User not found"}, 400