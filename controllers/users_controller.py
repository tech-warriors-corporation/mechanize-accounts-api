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

    def create(self):
        try:
            data = request.get_json()
            id = self.__users_service.create(data['name'], data['email'], data['password'], data['role'])

            return generate_response(id, 201)
        except Exception as error:
            return generate_response(str(error), 400)
