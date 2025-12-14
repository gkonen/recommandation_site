from flask import Blueprint, request
from utils.decorators import with_session
from utils.movie_factory import MovieFactory


movie_route = Blueprint('movie_route', __name__, url_prefix='/movies')

@movie_route.route('')
@with_session(factory_func=MovieFactory.get_controller)
def get_all_movies(controller):
    # Extract query parameters from the URL
    title = request.args.get('title')
    year = request.args.get('year', type=int)  # Convert to int if provided
    genre_name = request.args.get('genre_name')

    # Pagination parameters
    page = request.args.get('page', default=1, type=int)
    per_page = request.args.get('per_page', default=50, type=int)

    # Validate pagination parameters
    if page < 1:
        page = 1
    if per_page < 1 or per_page > 100:  # Max 100 items per page
        per_page = 50
    
    return controller.get_all_movies(
        title=title,
        year=year,
        genre_name=genre_name,
        page=page,
        per_page=per_page
    )

@movie_route.route('/<int:movie_id>', methods=['GET'])
@with_session(factory_func=MovieFactory.get_controller)
def get_movie(controller, movie_id):
    return controller.get_movie(movie_id)

@movie_route.route('/rating/<int:movie_id>', methods=['POST'])
@with_session(factory_func=MovieFactory.get_controller)
def rating_movie(controller, movie_id):
    """
    Expected JSON body:
    {
        "user_id": 42,
        "rating": 3
    }
    """
    data = request.get_json()

    if not data:
        return {"error": "No data provided"}, 400

    user_id = data.get('user_id')
    rating = data.get('rating')

    controller.post_rating_on_movie(movie_id, user_id, rating)
    return {"message": "Rating posted successfully"}, 201

