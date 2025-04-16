class AppError(Exception):
    pass


class NotFoundException(AppError):
    pass


class UsersNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__('Users not found')


class UserNotFoundException(NotFoundException):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f'User with id {user_id} not found in db')
