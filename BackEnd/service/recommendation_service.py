from utils.recommendation import Recommendation
import pandas as pd

class RecommendationService:
    def __init__(self, user_repository, movie_repository, recommendation):
        self.user_repository = user_repository
        self.movie_repository = movie_repository
        self.recommandation : Recommendation = recommendation

    #region RECOMMENDATION CONTENT-BASED
    def get_recommendations_for_user(self, user_id, limit=25):
        """
        Generate movie recommendations for a user.
        
        Algorithm:
        1. Get movies user rated >= 3 (6 in our database, max 5 movies)
        2. If found: apply algorithm to get recommended movie IDs
        3. If not found: return top 20 movies by score
        
        Args:
            user_id: The user's ID
            limit: Maximum number of recommendations
            
        Returns:
            List of recommended Movie objects
        """
        # Check if user exists
        if not self.user_repository.get_user(user_id):
            raise ValueError(f"User {user_id} not found")
        
        # Get movies user rated >= 3 (up to 5)
        highly_rated_ids = self.user_repository.get_highly_rated_movies_by_user(
            user_id, 
            min_rating=6,
            limit=5
        )
        
        # If user has no high ratings, return top 20 movies
        if not highly_rated_ids:
            print("No highly rated movies found, returning top 20 movies")
            return self._get_top_catalog_movies()
        
        # Get recommendations based on highly rated movies
        return self._get_personalized_recommendations(highly_rated_ids, user_id)
    
    def _get_top_catalog_movies(self):
        """
        Get the top 20 movies from the catalog by score.
        For users with no ratings >= 3.
        """
        return self.movie_repository.get_top_rated_movies(limit=20)
    
    def _get_personalized_recommendations(self, fave_ids, user_id):
        """
        Get personalized recommendations based on favorite (=highly rated) movies.
        
        Args:
            fave_ids: List of movie IDs user rated highly
            user_id: User ID (to exclude already rated movies)
        """
        all_recommended_ids = self.recommandation.recommend_for_user(fave_ids)
        
        # # For each highly-rated movie, get recommendations
        # for movie_id in fave_ids:
        #     recommended_ids = self.recommend_for_user(movie_id)
        #     all_recommended_ids.extend(recommended_ids)
        
        # # Remove duplicates
        # seen = set()
        # unique_ids = []
        # for movie_id in all_recommended_ids:
        #     if movie_id not in seen:
        #         seen.add(movie_id)
        #         unique_ids.append(movie_id)
        
        # # Remove favorite movies from recommendations
        # unique_ids = [mid for mid in unique_ids if mid not in fave_ids]
        
        # Remove movies user has already rated
        user_rated_ids = set(r.movie_id for r in self.user_repository.get_ratings_by_user(user_id))
        all_recommended_ids = [mid for mid in all_recommended_ids if mid not in user_rated_ids]
        
        # Get full movie objects
        if not all_recommended_ids:
            return []
        
        recommended_movies = self.movie_repository.get_movies_by_ids(all_recommended_ids)
        
        return recommended_movies

    #endregion

    #region RECOMMENDATION CF USER-BASED
    def get_recommendation_by_knn(self, user_id, k=5):
        list_rating = self.user_repository.get_ratings_by_user(user_id)  # movie_id, user_id, rating
        rows = [{"movieId": rating.movie_id, "userId": rating.user_id, "rating": rating.rating} for rating in
                list_rating]
        user_history = pd.DataFrame(rows)
        vector = self.recommandation.vectorize_user(user_history)
        print(vector)
        list_movie_id = self.recommandation.recommend_for_user_using_knn(user_id, vector, k)
        return self.movie_repository.get_movies_by_ids(list_movie_id)






