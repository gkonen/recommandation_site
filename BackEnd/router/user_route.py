from flask import Blueprint, request
from utils.decorators import with_session
from utils.user_factory import UserFactory

user_route = Blueprint('user_route', __name__, url_prefix='/users')

@user_route.route('')
@with_session(factory_func=UserFactory.get_controller)
def get_users(controller):
    return controller.get_all_users()

@user_route.route('/<int:user_id>')
@with_session(factory_func=UserFactory.get_controller)
def get_user_data(controller, user_id):
    return controller.get_user_data(user_id)

@user_route.route('/login', methods=['POST'])
@with_session(factory_func=UserFactory.get_controller)
def login(controller):
    """
    Authenticate a user.
    
    Expected JSON body:
    {
        "username": "jane_doe",
        "password": "secret123"
    }
    
    Returns:
    {
        "logged": true|false,
        "id": user_id|null
    }
    """
    data = request.get_json()
    
    if not data:
        return {"logged": False, "id": None, "error": "No data provided"}, 400
    
    username = data.get('username')
    password = data.get('password')
    
    return controller.authenticate_user(username, password)


# ### ROUTE FOR TESTING
# @user_route.route('/debug/<username>')
# @with_session(factory_func=UserFactory.get_controller)
# def debug_user(controller, username):
#     user = controller._UserController__repository.get_user_by_username(username)
#     if user:
#         return {
#             "found": True,
#             "user_id": user.user_id,
#             "username": user.username,
#             "password_in_db": user.pw
#         }
#     return {"found": False}, 404