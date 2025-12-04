from controller.user_controller import UserController
from repository.user_repository import UserRepository


class UserFactory:

    @staticmethod
    def get_controller(session):
        user_repository = UserRepository(session)
        user_controller = UserController(user_repository)
        return user_controller
