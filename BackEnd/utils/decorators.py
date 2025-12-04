
from functools import wraps
from database.config.db_session import DBSession

def with_session(factory_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                with DBSession() as session:
                    controller = factory_func(session)
                    return func(controller, *args, **kwargs)
            except Exception as e:
                print(f"Erreur lors de la récupération des films: {e}")
                return {"error": "Erreur serveur"}, 500
        return wrapper
    return decorator
