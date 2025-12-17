import numpy as np
import pandas as pd

from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.neighbors import NearestNeighbors

class Recommendation:

    _data_loaded = False
    _movies_df: pd.DataFrame | None = None
    _ratings_df: pd.DataFrame | None = None
    _user_preferences_df: pd.DataFrame | None = None

    _movie_encoded = None
    _row_norm_cache: np.ndarray | None = None
    _movie_ids: np.ndarray | None = None
    _id_to_idx: dict[int, int] | None = None

    @classmethod
    def _data_loader(cls):
        if cls._data_loaded:
            return
        print("Loading movie from csv ...")
        cls._movies_df = pd.read_csv('data/csv_files/movies.csv')
        print("Loading Movies successfully")

        print("Loading ratings from csv ...")
        cls._ratings_df = pd.read_csv('data/csv_files/ratings.csv')
        print("Loading ratings successfully")

        print("Loading user_preferencies from pickle ...")
        cls._user_preferences_df = pd.read_pickle('data/pickle_files/user_preferencies.pkl')
        print("Loading user_preferencies successfully")

        print("Preprocessing data ...")
        cls._preprocess_movies()
        cls._preprocess_ratings()
        print("Preprocessing data successfully")
        print("Data loaded successfully")
        cls._data_loaded = True

    @classmethod
    def _preprocess_movies(cls):
        cls._movies_df['list'] = pd.Series(cls._movies_df['genres'].str.split('|'))
        cls._movies_df = cls._movies_df.drop(columns=['genres'])

        mlb = MultiLabelBinarizer(sparse_output=True)
        cls._movie_encoded = mlb.fit_transform(cls._movies_df["list"])
        cls._row_norm_cache = np.sqrt(cls._movie_encoded.multiply(cls._movie_encoded).sum(axis=1)).A1

        cls._movie_ids = cls._movies_df["movieId"].to_numpy()
        cls._id_to_idx = {int(mv_id): i for i, mv_id in enumerate(cls._movie_ids)}


    @classmethod
    def _preprocess_ratings(cls):
        pass

    def recommend_for_user(self, list_movie: list[int], k: int = 5):
        self._data_loader()
        recommend_dict : dict[int, float] = {}
        # For evert mmovie in list_movie, we search the k most similar movies
        for search_movie_id in list_movie:
            similar_movies, scores = self._similar_movies(search_movie_id, k=k)
            for movie_id, score in zip(similar_movies, scores):
                # if existent one, I take the max of the two with a default valence of -inf if non existent
                recommend_dict[movie_id] = max(recommend_dict.get(movie_id, float("-inf")), score)
        # drop the movies already in the list
        for search_movie_id in list_movie:
            recommend_dict.pop(search_movie_id, None)
        sorted_recommend_dict = dict(sorted(recommend_dict.items(), key=lambda item: item[1], reverse=True))

        # return id of the movies find in our dictionary
        return [movie_id for movie_id, _ in sorted_recommend_dict.items()]


    def _similar_movies(self, film_id: int, k: int = 5):
        # Business variable
        # retrieve locally class variables
        movie_ids = type(self)._movie_ids
        id_to_idx = type(self)._id_to_idx
        movie_enc = type(self)._movie_encoded
        row_norms = type(self)._row_norm_cache

        i = id_to_idx[film_id]
        m_i = movie_enc.getrow(i)

        # numerateur: dot(m_i, movie_genre_token.T)
        # sur des lignes de 0 ou de 1, revient à un len(intersect)
        dots = m_i @ movie_enc.T
        dots = dots.toarray().ravel()

        # denom: ||xi|| * ||xj||
        denom = (row_norms[i] * row_norms)

        scores = np.divide(dots, denom, out=np.zeros_like(dots, dtype=float), where=denom != 0)

        scores[i] = -1.0  # exclure lui-même

        idx = np.argpartition(scores, -k)[-k:]
        idx = idx[np.argsort(scores[idx])[::-1]]

        return movie_ids[idx], scores[idx]

    def recommend_for_user_using_knn(self, user_id, user_vector, k: int = 5):
        # add the user vector to the dataframe
        user_vector_aligned = user_vector.reindex(
            columns=type(self)._user_preferences_df.columns,
            fill_value=0
        )
        type(self)._user_preferences_df = pd.concat(
            [type(self)._user_preferences_df, user_vector_aligned],
            ignore_index=False
        ).fillna(0)
        # loading data
        matrice = type(self)._user_preferences_df.to_numpy(dtype=np.float32)
        user_ids = type(self)._user_preferences_df.index.to_numpy()
        ratings = type(self)._ratings_df
        pos = {u: i for i, u in enumerate(user_ids)}
        # fit the model
        NN = NearestNeighbors(n_neighbors=k + 1, metric='cosine', algorithm='brute')
        NN.fit(matrice)

        # retrieve from the model the nearest user in our dataframe
        i = pos[user_id]
        dist, ind = NN.kneighbors(matrice[i:i + 1], n_neighbors=k + 1)
        ind = ind.ravel()
        mask = ind != i
        ind = ind[mask][:k]
        similar_user = user_ids[ind]

        movie_recommendation = []
        for u_id in similar_user:
            most_rated = ratings[ratings["userId"] == u_id].sort_values(by=["rating"], ascending=False).head(k)["movieId"].to_numpy()
            movie_recommendation.extend(most_rated)

        return list(set(movie_recommendation))

    def vectorize_user(self, rating_user):
        movies_clean = type(self)._movies_df.copy()

        score_df = pd.merge(rating_user, movies_clean, on="movieId")
        score_df = score_df.explode("list")
        score_df = score_df.rename(columns={"list": "genres"})
        score_df = score_df.drop(columns=["title"])

        vector_score = pd.pivot_table(score_df, index=["userId"], columns=["genres"], values="rating",
                                      aggfunc=lambda s: np.where(s > 2.5, 1, -1).sum()).fillna(0)
        vector_score['count'] = vector_score.abs().sum(axis=1)
        vector_score = vector_score.div(vector_score['count'], axis=0).round(2)
        vector_score = vector_score.drop(columns=['count'])
        return vector_score