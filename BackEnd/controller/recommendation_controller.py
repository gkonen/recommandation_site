from service.recommendation_service import RecommendationService

class RecommendationController:
    def __init__(self, recommendation_service: RecommendationService):
        self.__service = recommendation_service
    
    def get_recommendations(self, user_id, limit=25):
        """
        Get movie recommendations for a user.
        
        Args:
            user_id: The user's ID
            limit: Maximum number of recommendations (default: 25)
            
        Returns:
            Tuple of (response dict, status code)
        """
        try:
            self.__service.get_recommendation_by_knn(user_id, limit)
            #print(test[0].movie_id, test[0].user_id, test[0].rating )

            recommendations = self.__service.get_recommendations_for_user(user_id, limit)
            recommended_movies = [self._serialize_movie(m) for m in recommendations]
            return {
                "user_id": user_id,
                "movies": recommended_movies,
                "count": len(recommendations)
            }, 200
            
        except ValueError as e:
            # User not found
            return {"error": str(e)}, 404
        except Exception as e:
            return {"error": f"Failed to generate recommendations: {str(e)}"}, 500
    
    def _serialize_movie(self, movie):
        """
        Serialize movie in the same format as catalog items.
        Matches the format from MovieController.get_all_movies() except pagination-related info.
        """
        score = movie.score.rating if movie.score else None
        genre_list = [g.genre_name for g in movie.genres]
        tags = [tag.clean_tag for tag in movie.tags]
        return {
            "id": movie.movie_id,
            "title": movie.title,
            "year": movie.year,
            "score": score,
            "genres": genre_list,
            "tags": tags
        }