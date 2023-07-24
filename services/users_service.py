from repositories.user_repository import UserRepository
from os import environ
from enum import Enum
from re import match
import bcrypt
from enums.user_role_enum import UserRoleEnum
from texts import sanitize

class UsersService:
    __charset = 'utf-8'

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

        salt = bcrypt.hashpw(environ.get('CRYPTOCODE_PASSWORD').encode(self.__charset), bcrypt.gensalt()).decode(self.__charset)
        hashed_password = bcrypt.hashpw(password.encode(self.__charset), salt.encode(self.__charset)).decode(self.__charset)
        name = sanitize(name)
        email = sanitize(email)

        return self.__user_repository.create(name, email, hashed_password, role)

    def get(self, id: int):
        if not id:
            raise ValueError('Id is required')

        if not isinstance(id, int):
            raise ValueError('Id should be integer')

        return self.__user_repository.get(id)

    def get_by_email(self, email: str):
        if not email:
            raise ValueError('Email is required')

        if not isinstance(email, str):
            raise ValueError('Email should be string')

        email = sanitize(email)

        return self.__user_repository.get_by_email(email)

    def authenticate(self, email: str, password: str):
        if not self.__is_valid_email(email):
            raise ValueError('Invalid email')

        email = sanitize(email)
        user = self.__user_repository.get_by_email(email)

        if not user or not bcrypt.checkpw(password.encode(self.__charset), user['password'].encode(self.__charset)):
            raise ValueError('Invalid credentials')

        return user

    def get_user_by_token(self, token: str):
        if not token:
            raise ValueError('Token is required')

        return self.__user_repository.get_user_by_token(token)

    def get_id_by_token(self, token: str):
        return self.__user_repository.get_id_by_token(token)

    def get_user_name_by_id(self, id: int) -> str:
        if not id:
            raise ValueError('Id is required')

        if not isinstance(id, int):
            raise ValueError('Id should be integer')

        return self.__user_repository.get_user_name_by_id(id)

    def __is_valid_password(self, password: str) -> bool:
        return len(password) >= 8 and \
               any(char.isupper() for char in password) and \
               any(char.islower() for char in password) and \
               any(char.isdigit() for char in password)

    def __is_valid_email(self, email: str) -> bool:
        return match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email) is not None
