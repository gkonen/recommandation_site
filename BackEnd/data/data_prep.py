import numpy as np
import pandas as pd


CSV_PATH = 'data/csv_files/'
PKL_PATH = 'data/pickle_files/'


def prep_genres_df() -> pd.DataFrame:

    genre_list = [ "Action", "Adventure", "Animation", "Children", "Comedy", "Crime", "Documentary", "Drama", "Fantasy", "Film-Noir", "Horror", "IMAX", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western", "(no genres listed)" ]
    genres_df = pd.DataFrame({'genre_id': np.arange(1, len(genre_list)+1), 'genre_name': genre_list })
    return genres_df

def prep_movies_df() -> tuple[pd.DataFrame, pd.DataFrame]:

    movies = pd.read_csv(f'{CSV_PATH}movies.csv')

    # separate 'year' from 'title'
    movies['year'] = movies['title'].str.extract(r'\((\d{4})\)\s*$')
    movies['title'] = movies['title'].str.replace(r'\s*\(\d{4}\)\s*$', '', regex=True)

    # convert 'year' from sting to numeric
    movies['year'] = pd.to_numeric(movies['year'], errors='coerce')

    # make new column with movie's genres into an array
    movies['genres_list'] = pd.Series(movies['genres'].str.split('|'))

    # rename id column to 'movie_id'
    movies.rename(columns={'movieId':'movie_id'}, inplace=True)

    # prepare 'expanded_movies' df, needed to create the movie_genre_df
    expanded_movies = movies.explode('genres_list')

    # select relevant columns
    movies_df = movies[['movie_id', 'title', 'year']]
    
    return movies_df, expanded_movies

def prep_movie_genre_df(exp_movies: pd.DataFrame, genres: pd.DataFrame) -> pd.DataFrame:

    joint_movie_genre_df = exp_movies.merge(right=genres, how='inner', left_on='genres_list', right_on='genre_name')
    movie_genre_df = joint_movie_genre_df[['movie_id', 'genre_id']]

    return movie_genre_df

def prep_tags_df() -> pd.DataFrame:

    tags_df = pd.read_csv(f'{CSV_PATH}tags.csv')
    tags_df.rename(columns={'userId':'user_id', 'movieId':'movie_id', 'timestamp':'recorded_at'}, inplace=True)
    return tags_df

def prep_ratings_df() -> pd.DataFrame:

    ratings_df = pd.read_csv(f'{CSV_PATH}ratings.csv')
    ratings_df['rating'] = ratings_df['rating'].apply(lambda x: x*2).astype(int)
    ratings_df.rename(columns={'userId':'user_id', 'movieId':'movie_id', 'timestamp':'recorded_at'}, inplace=True)
    return ratings_df

def prep_user_df(ratings: pd.DataFrame) -> pd.DataFrame:
    user_id = ratings['user_id'].unique()
    app_user_df = pd.DataFrame([], columns=['user_id', 'username', 'pw'])
    app_user_df['user_id'] = user_id
    return app_user_df

def main() -> None:
    genres_df = prep_genres_df()
    genres_df.to_pickle(f'{PKL_PATH}genre.pkl')

    movie_tuple = prep_movies_df()
    movies_df = movie_tuple[0]
    exp_movies_df = movie_tuple[1]
    movies_df.to_pickle(f'{PKL_PATH}movie.pkl')

    movie_genre_df = prep_movie_genre_df(exp_movies_df, genres_df)
    movie_genre_df.to_pickle(f'{PKL_PATH}movie_genre.pkl')

    tag_df = prep_tags_df()
    tag_df.to_pickle(f'{PKL_PATH}tag.pkl')

    ratings_df = prep_ratings_df()
    ratings_df.to_pickle(f'{PKL_PATH}rating.pkl')

    user_df = prep_user_df(ratings_df)
    user_df.to_pickle(f'{PKL_PATH}app_user.pkl')

    print('Data prepared/transformed and saved.')

if __name__ == '__main__':
    main()