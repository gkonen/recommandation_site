from flask import Blueprint
from utils.decorators import with_session
from utils.recommendation_factory import RecommendationFactory

recommendation_route = Blueprint('recommendation_route', __name__, url_prefix='/recommendations')

@recommendation_route.route('/<int:user_id>', methods=['GET'])
@with_session(factory_func=RecommendationFactory.get_controller)
def get_user_recommendations(controller, user_id):
    return controller.get_recommendations(user_id)