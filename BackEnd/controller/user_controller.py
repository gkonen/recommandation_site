from repository.user_repository import UserRepository

class UserController:
    def __init__(self, user_repository : UserRepository):
        self.__repository = user_repository

    def get_all_users(self):
        return self.__repository.get_all_users()

    def get_user(self, user_id):
        user = self.__repository.get_user(user_id)
        if user is not None:
            return {"id": user.user_id, "username": user.username}, 200
        else:
            return {"error" : "User not found"}, 400
        
    def authenticate_user(self, username, password):
        """
        Authenticate a user with username and password.
        
        Args:
            username: The username provided
            password: The password provided
            
        Returns:
            Tuple of (response dict, status code)
        """
        if not username or not password:
            return {"logged": False, "id": None, "error": "Username and password required"}, 400
        
        user = self.__repository.get_user_by_username(username)
        
        if user is None:
            return {"logged": False, "id": None}, 401
        
        if user.password == password:
            return {"logged": True, "id": user.user_id}, 200
        else:
            return {"logged": False, "id": None}, 401