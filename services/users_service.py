from repositories.user_repository import UserRepository
from cryptocode import encrypt
from os import environ
from enum import Enum
from re import match

class UserRoleEnum(Enum):
    DRIVER = 'driver'
    MECHANIC = 'mechanic'

class UsersService:
    def __init__(self, user_repository: UserRepository):
        self.__user_repository = user_repository

    def create(self, name: str, email: str, password: str, role: UserRoleEnum) -> int:
        if not name:
            raise ValueError('Name is required')

        if not self.__is_valid_email(email):
            raise ValueError('Invalid email')

        if not self.__is_valid_password(password):
            raise ValueError('Password must be at least 8 characters and contain at least one uppercase letter, one lowercase letter and one digit')

        if role != UserRoleEnum.DRIVER.value and role != UserRoleEnum.MECHANIC.value:
            raise ValueError('Role is invalid')

        return self.__user_repository.create(name, email, encrypt(password, environ.get("CRYPTOCODE_PASSWORD")), role)

    def get(self, id: int):
        if not id:
            raise ValueError('Id is required')

        if not isinstance(id, int):
            raise ValueError('Id should be integer')

        return self.__user_repository.get(id)

    def __is_valid_password(self, password: str) -> bool:
        return len(password) >= 8 and \
               any(char.isupper() for char in password) and \
               any(char.islower() for char in password) and \
               any(char.isdigit() for char in password)

    def __is_valid_email(self, email: str) -> bool:
        return match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None
