import pandas as pd
from sqlalchemy import text
from database.config.db_engine import DBEngine

# database tables names in proper insertion order
DB_TABLES = ['genre', 'movie', 'movie_genre', 'app_user', 'tag', 'rating']

PKL_PATH = 'pickle_files/'
ENGINE = DBEngine.get_engine()

def truncate_tables():
    """
    Truncate all tables in reverse order to respect foreign key constraints.
    Uses CASCADE to handle dependencies.
    """
    # Reverse order for truncation to avoid FK constraint violations
    reversed_tables = list(reversed(DB_TABLES))
    
    try:
        with ENGINE.connect() as conn:
            print("Truncating existing tables...")
            for table_name in reversed_tables:
                # RESTART IDENTITY to reset auto-increment sequences
                # CASCADE to automatically truncate dependent tables
                conn.execute(text(f"TRUNCATE TABLE {table_name} RESTART IDENTITY CASCADE"))
                print(f"  - Truncated {table_name}")
            conn.commit()
            print("All tables truncated successfully!\n")
    except Exception as e:
        print(f"Error during table truncation: {e}")
        raise

def populate_db():
    """
    Populate database tables from pickle files.
    Truncates existing data before insertion to avoid primary key conflicts.
    """
    try:
        # Truncate all tables to avoid conflicts
        truncate_tables()
        
        # Insert data from pickle files
        for table_name in DB_TABLES:
            try:
                # Load data from pickle file
                pkl_file = f'{PKL_PATH}{table_name}.pkl'
                print(f'Loading data from {pkl_file}...')
                df = pd.read_pickle(pkl_file)
                
                # Insert data into database
                print(f'Inserting {len(df)} rows into {table_name}...')
                df.to_sql(
                    name=table_name,        # target table
                    con=ENGINE,             # SQLAlchemy engine
                    if_exists="append",     # append to existing table
                    index=False,            # ignore DataFrame index
                    method='multi',         # use multi-row INSERT for better performance
                    chunksize=1000          # insert in chunks for large datasets
                )
                print(f'  ✓ Successfully inserted {len(df)} rows into {table_name}\n')
                
            except FileNotFoundError:
                print(f'  ✗ Error: Pickle file not found for {table_name}\n')
                raise
                
            except Exception as e:
                print(f'  ✗ Error inserting data into {table_name}: {e}\n')
                raise
        
        print("=" * 50)
        print("Database population completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print("\n" + "=" * 50)
        print(f"Database population failed: {e}")
        print("=" * 50)
        raise

if __name__ == "__main__":
    try:
        populate_db()
    except Exception as e:
        print(f"\n  ✗ Script execution failed. Please check the errors above.")
        exit(1)