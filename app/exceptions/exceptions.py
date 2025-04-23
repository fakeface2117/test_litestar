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


class UserCarsNotFoundException(NotFoundException):
    def __init__(self, user_id):
        self.user_id = user_id
        super().__init__(f'Cars for user {user_id} not found in db')


class CarNotFoundException(NotFoundException):
    def __init__(self, car_id, user_id):
        self.user_id = user_id
        self.car_id = car_id
        super().__init__(f'Car with id {car_id} not found in database for user {user_id}')


class CarsNotFoundException(NotFoundException):
    def __init__(self):
        super().__init__('Cars not found')
