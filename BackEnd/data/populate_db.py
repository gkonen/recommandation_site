import pandas as pd
from database.engine.db_engine import DBEngine


# genres_df = pd.read_pickle('data/pickle_files/genres.pkl')
# genres_df.columns = ['genrename']

# movies_df = pd.read_pickle('data/pickle_files/movies.pkl')
# movies_df.columns = [col.lower() for col in movies_df.columns]
# movies_df['year'] = pd.to_numeric(movies_df['year'], errors='coerce')

movie_genre_df = pd.read_pickle('data/pickle_files/movie_genre.pkl')

app_user_df = pd.read_pickle('data/pickle_files/app_user.pkl')

ratings_df = pd.read_pickle('data/pickle_files/ratings.pkl')

if __name__ == "__main__":
    # Get the SQLAlchemy engine from your DBEngine module
    engine = DBEngine.get_engine()

    # Test insertion of the genres DataFrame
    print("Inserting into the database...")
    ratings_df.to_sql(
        name="rating",     # target table
        con=engine,             # the SQLAlchemy engine
        if_exists="append",     # append to the table (don't replace)
        index=False             # /!\ don't include the pandas index
    )
    print("Insertion complete!")