from flask_jwt_extended import create_access_token
from services.users_service import UsersService
from response import generate_response
from flask import request
from controllers.controller import Controller
from flask import Flask
from request import should_be_logged, has_valid_token, should_be_valid_client_id

class UsersController(Controller):
    def __init__(self, app: Flask, users_service: UsersService):
        super().__init__(app)

        self.__users_service = users_service

    def register_routes(self):
        self._app.add_url_rule('/api/accounts/users', 'create', self.create, methods=['POST'])
        self._app.add_url_rule('/api/accounts/login', 'login', self.login, methods=['POST'])
        self._app.add_url_rule('/api/accounts/has-valid-token', 'has_valid_token', self.has_valid_token, methods=['GET'])
        self._app.add_url_rule('/api/accounts/users/<int:id>', 'get', self.get, methods=['GET'])

    @should_be_valid_client_id
    def create(self):
        try:
            data = request.get_json()
            id = self.__users_service.create(data['name'], data['email'], data['password'], data['role'])

            return generate_response(id, 201)
        except Exception as error:
            return generate_response(str(error), 400)

    @should_be_valid_client_id
    def login(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')
            user = self.__users_service.authenticate(email, password)
            access_token = create_access_token(identity=user, expires_delta=False)

            return generate_response(
                {
                    "access_token": access_token,
                    "user": {
                        "id": user["id"],
                        "name": user["name"],
                        "role": user["role"],
                    }
                },
                200
            )
        except ValueError as error:
            return generate_response(str(error), 401)

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
    def get(self, id: int):
        try:
            user = self.__users_service.get(id)

            return generate_response(user, 200)
        except Exception as error:
            return generate_response(str(error), 400)
