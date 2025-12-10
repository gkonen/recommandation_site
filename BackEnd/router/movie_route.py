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

    return controller.get_all_movies(title=title, year=year, genre_name=genre_name)

@movie_route.route('/<int:movie_id>')
@with_session(factory_func=MovieFactory.get_controller)
def get_movie(controller, movie_id):
    return controller.get_movie(movie_id)


# ### TEST 
# @movie_route.route('/debug/<int:movie_id>')
# @with_session(factory_func=MovieFactory.get_controller)
# def debug_movie(controller, movie_id):
#     movie = controller._MovieController__repository.get_movie(movie_id)
#     if movie:
#         return {
#             "movie_id": movie.movie_id,
#             "title": movie.title,
#             "year": movie.year,
#             "genres": [g.genre_name for g in movie.genres],
#             "genre_count": len(movie.genres)
#         }
#     return {"error": "Movie not found"}, 404