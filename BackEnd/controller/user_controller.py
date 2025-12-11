from repository.user_repository import UserRepository

class UserController:
    def __init__(self, user_repository : UserRepository):
        self.__repository = user_repository

    def get_all_users(self):
        return self.__repository.get_all_users()

    def get_user(self, user_id):
        """
        Get a user by ID with their ratings and tags.
        
        Returns:
            Tuple of (response dict, status code)
        """
        # check if user exists
        user = self.__repository.get_user(user_id)
        
        if not user:
            return {"error": f"User with id #{user_id} not found"}, 404
        
        # user exists --> get their ratings and tags
        ratings = self.__repository.get_ratings_by_user(user_id)
        tags = self.__repository.get_tags_by_user(user_id)

        serialized_ratings = [ self._serialize_rating(r) for r in ratings ]
        serialized_tags = [ self._serialize_tag(t) for t in tags ]
        
        response = {
            "user_id": user.user_id,
            "username": user.username,
            "ratings": serialized_ratings,
            "ratings_count": len(ratings),
            "tags": serialized_tags,
            "tags_count": len(tags)
        }

        # Messages based on what's empty
        messages = []
        if not ratings:
            messages.append("User has no ratings yet")
        if not tags:
            messages.append("User has no tags yet")
        
        if messages:
            response["message"] = " + ".join(messages)
        
        return response, 200


    def _serialize_rating(self, rating):
        """ Serialize a Rating object to a dictionary """
        return {
            "movie_id": rating.movie_id,
            "movie_title": rating.movie.title,  # access through relationship
            "rating": rating.rating,
            "timestamp": rating.recorded_at
        }

    def _serialize_tag(self, tag):
        """ Serialize a Tag object to a dictionary """
        return {
            "movie_id": tag.movie_id,
            "movie_title": tag.movie.title,  # access through relationship
            "tag": tag.tag,
            "timestamp": tag.recorded_at
        }

        
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
