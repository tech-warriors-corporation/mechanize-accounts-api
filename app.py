import secrets
import base64
from flask_cors import CORS
from flask import Flask
from flask_jwt_extended import JWTManager
from os import environ
from dotenv import load_dotenv, find_dotenv
from controllers.users_controller import UsersController
from services.users_service import UsersService
from repositories.user_repository import UserRepository

charset = 'utf-8'
app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = environ.get('CRYPTOCODE_PASSWORD')

CORS(app, resources={f"/api/*": { "origins": "*" }})

JWTManager(app)

base64.b64encode(secrets.token_bytes(32)).decode(charset)

load_dotenv(find_dotenv())

UsersController(app, UsersService(UserRepository()))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=8000)
