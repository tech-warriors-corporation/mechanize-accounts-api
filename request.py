from flask import request
from response import generate_response
from flask_jwt_extended import decode_token
from database import get_connection
from os import environ
from enums.user_role_enum import UserRoleEnum

valid_client_id = environ.get('CLIENT_ID')

def has_valid_token(token: str):
    try:
        user = decode_token(token)['sub']
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id FROM users WHERE id={user['id']} AND name='{user['name']}' AND email='{user['email']}' AND password='{user['password']}' AND role='{user['role']}'")

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result is not None
    except:
        return False

def is_driver(token: str):
    try:
        user = decode_token(token)['sub']
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id FROM users WHERE email='{user['email']}' AND role='{UserRoleEnum.DRIVER.value}'")

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result is not None
    except:
        return False

def is_mechanic(token: str):
    try:
        user = decode_token(token)['sub']
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT id FROM users WHERE email='{user['email']}' AND role='{UserRoleEnum.MECHANIC.value}'")

        result = cursor.fetchone()

        cursor.close()
        connection.close()

        return result is not None
    except:
        return False

def should_be_logged(callback):
    def secure_function(*args, **kwargs):
        token = request.headers.get('Authorization')

        if token is not None and has_valid_token(token):
            return callback(*args, **kwargs)
        else:
            return generate_response(status_code=401)

    secure_function.__name__ = callback.__name__

    return secure_function

def should_be_valid_client_id(callback):
    def secure_function(*args, **kwargs):
        client_id = request.headers.get('clientId')

        if client_id == valid_client_id:
            return callback(*args, **kwargs)
        else:
            return generate_response(status_code=401)

    secure_function.__name__ = callback.__name__

    return secure_function
