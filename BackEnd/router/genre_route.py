from flask import Blueprint, request
from utils.decorators import with_session
from utils.genre_factory import GenreFactory

genre_route = Blueprint('genre', __name__, url_prefix='/genres')

@genre_route.route('')
@with_session(factory_func=GenreFactory.get_controller)
def get_all_genres(controller):
    return controller.get_all_genres()