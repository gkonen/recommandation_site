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
        
        if user.pw == password:
            return {"logged": True, "id": user.user_id}, 200
        else:
            return {"logged": False, "id": None}, 401
        
    def get_ratings_by_user(self, user_id):
        """
        Get all ratings for a specific user.
        
        Returns:
            Tuple of (response dict, status code)
        """
        # check if user exists
        if not self.__repository.user_exists(user_id):
            return {"error": "User not found"}, 404
        
        # user exists, get their ratings
        ratings = self.__repository.get_ratings_by_user(user_id)
        
        if not ratings:  # Empty list --> user has no ratings
            return {
                "user_id": user_id,
                "ratings": [],
                "message": "User has no ratings yet"
            }, 200
        
        # user has ratings
        serialized_ratings = [ self._serialize_rating(r) for r in ratings ]

        return {
            "user_id": user_id,
            "ratings": serialized_ratings,
            "count": len(ratings)
        }, 200

    def _serialize_rating(self, rating):
        """ Serialize a Rating object to a dictionary """
        return {
            "movie_id": rating.movie_id,
            "movie_title": rating.movie.title,  # access through relationship
            "rating": rating.rating,
            "timestamp": rating.timestamp  # adjust based on your Rating model
        }
    
    def get_tags_by_user(self, user_id):
        """
        Get all tags for a specific user.
        
        Returns:
            Tuple of (response dict, status code)
        """
        # check if user exists
        if not self.__repository.user_exists(user_id):
            return {"error": "User not found"}, 404
        
        # user exists, get their tags
        tags = self.__repository.get_tags_by_user(user_id)
        
        if not tags:  # Empty list --> user has no tags
            return {
                "user_id": user_id,
                "tags": [],
                "message": "User has no tags yet"
            }, 200
        
        # user has tags
        serialized_tags = [ self._serialize_tag(t) for t in tags ]

        return {
            "user_id": user_id,
            "tags": serialized_tags,
            "count": len(tags)
        }, 200

    def _serialize_tag(self, tag):
        """ Serialize a Tag object to a dictionary """
        return {
            "movie_id": tag.movie_id,
            "movie_title": tag.movie.title,  # access through relationship
            "tag": tag.tag,
            "timestamp": tag.timestamp  # adjust based on your Tag model
        }
    