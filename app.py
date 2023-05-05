import secrets
import base64
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from controllers.users_controller import UsersController
from services.users_service import UsersService
from repositories.user_repository import UserRepository
from os import environ


from flask_jwt_extended import JWTManager, create_access_token
from flask import Flask, jsonify, request

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = environ.get('CRYPTOCODE_PASSWORD')  # read from .env
CORS(app, resources={f"/api/*": { "origins": "*" }})

# Setting the JWT
jwt = JWTManager(app)
key = base64.b64encode(secrets.token_bytes(32)).decode('utf-8')

load_dotenv(find_dotenv())

UsersController(app, UsersService(UserRepository()))


if __name__ == '__main__':
    app.run(debug=True, port=8000)
