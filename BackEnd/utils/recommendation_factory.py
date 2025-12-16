from flask import current_app
from controller.recommendation_controller import RecommendationController
from service.recommendation_service import RecommendationService
from repository.user_repository import UserRepository
from repository.movie_repository import MovieRepository

class RecommendationFactory:
    @staticmethod
    def get_controller(session):
        """
        Create and return a RecommendationController with all dependencies.
        """
        user_repository = UserRepository(session)
        movie_repository = MovieRepository(session)
        recommendation_service = RecommendationService(user_repository, movie_repository, current_app.extensions['recommendation'])
        controller = RecommendationController(recommendation_service)
        return controller