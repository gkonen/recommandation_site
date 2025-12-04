from flask import Blueprint
from utils.decorators import with_session
from utils.movie_factory import MovieFactory

movie_route = Blueprint('movie_route', __name__, url_prefix='/movie')

@movie_route.route('')
@with_session(factory_func=MovieFactory.get_controller)
def get_all_movies(controller):
    return controller.get_all_movies()

@movie_route.route('/<int:movie_id>')
@with_session(factory_func=MovieFactory.get_controller)
def get_movie(controller, movie_id):
    return controller.get_movie(movie_id)