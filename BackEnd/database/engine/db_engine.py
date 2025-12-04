from sqlalchemy import create_engine

import os
from dotenv import load_dotenv

load_dotenv()

class DBEngine:
    __engine = None

    @staticmethod
    def get_engine():
        if DBEngine.__engine is None:
            name = os.getenv("DB_NAME")
            host = os.getenv("DB_HOST")
            port = os.getenv("DB_PORT")
            user = os.getenv("DB_USER")
            password = os.getenv("DB_PASSWORD")
            DBEngine.__engine = create_engine(f"postgresql+psycopg://{user}:{password}@{host}:{port}/{name}")
        return DBEngine.__engine


if __name__ == "__main__":
    DBEngine.get_engine()
