from flask_jwt_extended import create_access_token
from services.users_service import UsersService
from response import generate_response
from flask import request
from controllers.controller import Controller
from flask import Flask
from request import should_be_logged, has_valid_token, should_be_valid_client_id, is_driver, is_mechanic

class UsersController(Controller):
    def __init__(self, app: Flask, users_service: UsersService):
        super().__init__(app)

        self.__users_service = users_service

    def register_routes(self):
        self._app.add_url_rule('/api/accounts/users', 'create', self.create, methods=['POST'])
        self._app.add_url_rule('/api/accounts/login', 'login', self.login, methods=['POST'])
        self._app.add_url_rule('/api/accounts/has-valid-token', 'has_valid_token', self.has_valid_token, methods=['GET'])
        self._app.add_url_rule('/api/accounts/get-user-by-token', 'get_user_by_token', self.get_user_by_token, methods=['GET'])
        self._app.add_url_rule('/api/accounts/get-id-by-token', 'get_id_by_token', self.get_id_by_token, methods=['GET'])
        self._app.add_url_rule('/api/accounts/is-driver', 'is_driver', self.is_driver, methods=['GET'])
        self._app.add_url_rule('/api/accounts/is-mechanic', 'is_mechanic', self.is_mechanic, methods=['GET'])
        self._app.add_url_rule('/api/accounts/users/<int:id>', 'get', self.get, methods=['GET'])
        self._app.add_url_rule('/api/accounts/users/<int:id>/user-name', 'get_user_name_by_id', self.get_user_name_by_id, methods=['GET'])
        self._app.add_url_rule('/api/accounts/change-password', 'change_password', self.change_password, methods=['PATCH'])

    @should_be_valid_client_id
    def create(self):
        try:
            data = request.get_json()
            id = self.__users_service.create(data['name'], data['email'], data['password'], data['role'])

            return generate_response(id, 201)
        except Exception as error:
            print(error)
            return generate_response(status_code=400)

    @should_be_valid_client_id
    def login(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            user = self.__users_service.authenticate(email, password)

            return generate_response(self.__mount_user_response(user), 200)
        except Exception as error:
            print(error)
            return generate_response(status_code=401)

    @should_be_valid_client_id
    def get_user_by_token(self):
        try:
            token = request.headers.get('Authorization')
            user = self.__users_service.get_user_by_token(token)

            if not user:
                return generate_response(status_code=400)

            return generate_response(self.__mount_user_response(user), 200)
        except:
            return generate_response(status_code=400)

    @should_be_valid_client_id
    @should_be_logged
    def get_id_by_token(self):
        try:
            token = request.headers.get('Authorization')

            return generate_response(self.__users_service.get_id_by_token(token), 200)
        except Exception as error:
            print(error)
            return generate_response(status_code=400)

    @should_be_valid_client_id
    def has_valid_token(self):
        try:
            token = request.headers.get('Authorization')
            is_valid_token = has_valid_token(token)

            if not is_valid_token:
                return generate_response(False, 498)

            return generate_response(True, 200)
        except:
            return generate_response(False, 498)

    @should_be_valid_client_id
    @should_be_logged
    def is_driver(self):
        try:
            token = request.headers.get('Authorization')

            if not is_driver(token):
                return generate_response(False, 401)

            return generate_response(True, 200)
        except:
            return generate_response(False, 401)

    @should_be_valid_client_id
    @should_be_logged
    def is_mechanic(self):
        try:
            token = request.headers.get('Authorization')

            if not is_mechanic(token):
                return generate_response(False, 401)

            return generate_response(True, 200)
        except:
            return generate_response(False, 401)

    @should_be_valid_client_id
    @should_be_logged
    def get(self, id: int):
        try:
            user = self.__users_service.get(id)

            return generate_response(user, 200)
        except Exception as error:
            print(error)
            return generate_response(status_code=400)

    @should_be_valid_client_id
    @should_be_logged
    def get_user_name_by_id(self, id: int):
        try:
            return generate_response(self.__users_service.get_user_name_by_id(id), 200)
        except Exception as error:
            print(error)
            return generate_response(status_code=400)

    @should_be_valid_client_id
    @should_be_logged
    def change_password(self):
        try:
            data = request.get_json()
            token = request.headers.get('Authorization')
            user = self.__users_service.get_user_by_token(token)
            result = self.__users_service.change_password(user['id'], data['current_password'], data['new_password'], data['new_password_confirmation'])

            if result:
                user = self.__users_service.get_by_email(user['email'])

            return generate_response(
                { 'changed': result, 'data': self.__mount_user_response(user) if result else None, 'error_type': None },
                200 if result else 206
            )
        except Exception as error:
            return generate_response({ 'changed': False, 'data': None, 'error_type': str(error) }, 206)

    def __mount_user_response(self, user):
        return {
            "access_token": create_access_token(identity=user, expires_delta=False),
            "user": {
                "id": user["id"],
                "name": user["name"],
                "role": user["role"],
            }
        }
