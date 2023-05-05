from flask_jwt_extended import create_access_token
from services.users_service import UsersService
from response import generate_response
from flask import request
from controllers.controller import Controller
from flask import Flask

class UsersController(Controller):
    def __init__(self, app: Flask, users_service: UsersService):
        super().__init__(app)

        self.__users_service = users_service

    def register_routes(self):
        self._app.add_url_rule('/api/accounts/users', 'create', self.create, methods=['POST'])
        self._app.add_url_rule('/api/accounts/users/<int:id>', 'get', self.get, methods=['GET'])
        self._app.add_url_rule('/api/accounts/login', 'login', self.login, methods=['POST'])
        self._app.add_url_rule('/api/accounts/users/getByEmail/<string:email>', 'get_by_email', self.get_by_email, methods=['GET'])

    def create(self):
        try:
            data = request.get_json()
            id = self.__users_service.create(data['name'], data['email'], data['password'], data['role'])

            return generate_response(id, 201)
        except Exception as error:
            return generate_response(str(error), 400)

    def get(self, id: int):
        try:
            user = self.__users_service.get(id)

            return generate_response(user, 200)
        except Exception as error:
            return generate_response(str(error), 400)

    def login(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user_id = self.__users_service.authenticate(email, password)
            access_token = create_access_token(identity=user_id)

            return generate_response({"access_token": access_token}, 200)
        except ValueError as error:
            return generate_response(str(error), 400)


    def get_by_email(self, email: str):
        try:
            user = self.__users_service.get_by_email(email)

            return generate_response(user, 200)
        except Exception as error:
            return generate_response(str(error), 400)