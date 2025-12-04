from flask import Blueprint
from utils.decorators import with_session
from utils.user_factory import UserFactory

user_route = Blueprint('user_route', __name__, url_prefix='/user')

@user_route.route('')
@with_session(factory_func=UserFactory.get_controller)
def get_users(controller):
    return controller.get_all_users()

@user_route.route('/<int:user_id>')
@with_session(factory_func=UserFactory.get_controller)
def get_user(controller, user_id):
    return controller.get_user(user_id)