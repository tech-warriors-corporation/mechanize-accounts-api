from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv, find_dotenv
from controllers.users_controller import UsersController
from services.users_service import UsersService
from repositories.user_repository import UserRepository

app = Flask(__name__)

CORS(app, resources={f"/api/*": { "origins": "*" }})

load_dotenv(find_dotenv())

UsersController(app, UsersService(UserRepository()))

if __name__ == '__main__':
    app.run(debug=True, port=8000)
