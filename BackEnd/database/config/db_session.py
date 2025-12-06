from sqlalchemy.orm import sessionmaker, Session
from database.config.db_engine import DBEngine

import traceback

class DBSession:
    def __init__(self):
        self._engine = DBEngine.get_engine()
        self._session_factory = sessionmaker(bind=self._engine)
        self._session_local = None

    def __enter__(self) -> Session:
        self._session_local = self._session_factory()
        return self._session_local

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._session_local:
            if exc_type is not None:
                self._session_local.rollback()
                print(f"Error occurred during request {exc_type.__name__}")
                traceback.print_exception(exc_type, exc_val, exc_tb)
            self._session_local.close()
        return False