
from flask import Flask
from database.config.db_session import DBSession
from database.models.models import Movie, Genre, AppUser, MovieGenre, Rating, Tag

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/movies')
def get_movies():
    try:
        with DBSession() as session:
            movies_list = session.query(Movie).all()
            return {"movies": [{"id": m.movieId, "title": m.title} for m in movies_list]}
    except Exception as e:
        print(f"Erreur lors de la récupération des films: {e}")
        return {"error": "Erreur serveur"}, 500

@app.route('/genre')
def get_genre():
    try:
        with DBSession() as session:
            genre_list = session.query(Genre).all()
            return {"genre": [{"id": genre.genreId, "name": genre.genreName} for genre in genre_list]}
    except Exception as e:
        print(f"Erreur lors de la récupération des genres: {e}")
        return {"error": "Erreur serveur"}, 500

@app.route("/user")
def get_users():
    try:
        with DBSession() as session:
            users_list = session.query(AppUser).all()
            return {"users": [{"id": user.userId, "username": user.username} for user in users_list]}
    except Exception as e:
        print(f"Erreur lors de la récupération des utilisateurs: {e}")
        return {"error": "Erreur serveur"}, 500

@app.route("/moviegenre")
def get_movie_genre():
    try:
        with DBSession() as session:
            moviegenre_list = session.query(MovieGenre).all()
            return {"moviegenre": [{"movieId": mg.movieId, "genreId": mg.genreId } for mg in moviegenre_list]}
    except Exception as e:
        print(f"Erreur lors de la récupération des movie_genre: {e}")
        return {"error": "Erreur serveur"}, 500

@app.route("/rating")
def get_rating():
    try:
        with DBSession() as session:
            rating_list = session.query(Rating).all()
            return {"rating": [{"userid": rt.userId, "movieid": rt.movieId, "rating": rt.rating} for rt in rating_list]}
    except Exception as e:
        print(f"Erreur lors de la récupération des rating: {e}")
        return {"error": "Erreur serveur"}, 500

@app.route("/tag")
def get_tag():
    try:
        with DBSession() as session:
            tag_list = session.query(Tag).all()
            return {"rating": [{"userid": tg.userId, "movieid": tg.movieId, "tag": tg.tag} for tg in tag_list]}
    except Exception as e:
        print(f"Erreur lors de la récupération des tags: {e}")
        return {"error": "Erreur serveur"}, 500



if __name__ == '__main__':
    app.run()
