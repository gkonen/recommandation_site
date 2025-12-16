from flask import Flask
from flask_cors import CORS

from router.movie_route import movie_route
from router.user_route import user_route
from router.genre_route import genre_route
from utils.recommendation import Recommendation
from router.recommendation_route import recommendation_route

app = Flask(__name__)
CORS(app)

recommendation = Recommendation()
recommendation._data_loader()
app.extensions['recommendation'] = recommendation

app.register_blueprint(movie_route)
app.register_blueprint(user_route)
app.register_blueprint(genre_route)
app.register_blueprint(recommendation_route)

# Keep this code as example of request to database
# @app.route('/movies')
# def get_movies():
#     try:
#         with DBSession() as session:
#             movies_list = session.query(Movie).all()
#             return {"movies": [{"id": m.movieId, "title": m.title} for m in movies_list]}
#     except Exception as e:
#         print(f"Erreur lors de la récupération des films: {e}")
#         return {"error": "Erreur serveur"}, 500


if __name__ == '__main__':
    app.run()
