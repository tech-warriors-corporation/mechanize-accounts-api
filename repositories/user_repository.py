from database import get_connection
from flask_jwt_extended import decode_token

class UserRepository:
    def __init__(self):
        self.__connection = None

    def create(self, name: str, email: str, password: str, role: str) -> int:
        self.__connection = get_connection()
        cursor = self.__connection.cursor()

        cursor.execute(f"INSERT INTO users (name, email, password, role) VALUES ('{name}', '{email}', '{password}', '{role}') RETURNING id")

        response = cursor.fetchone()
        id = response[0]

        self.__connection.commit()
        cursor.close()
        self.__connection.close()

        return id

    def get(self, id: int):
        self.__connection = get_connection()
        cursor = self.__connection.cursor()

        cursor.execute(f"SELECT name, email, role FROM users WHERE id = {id}")
        row = cursor.fetchone()
        user = { 'id': id, 'name': row[0], 'email': row[1], 'role': row[2] }

        cursor.close()
        self.__connection.close()

        return user

    def get_by_email(self, email: str):
        self.__connection = get_connection()
        cursor = self.__connection.cursor()

        cursor.execute(f"SELECT id, name, email, password, role FROM users WHERE email = '{email}'")

        row = cursor.fetchone()

        if not row:
            return None

        user = { 'id': row[0], 'name': row[1], 'email': row[2], 'password': row[3], 'role': row[4] }

        cursor.close()
        self.__connection.close()

        return user

    def get_user_by_token(self, token: str):
        self.__connection = get_connection()
        cursor = self.__connection.cursor()
        user_from_token = decode_token(token)['sub']

        cursor.execute(f"SELECT id, name, email, password, role FROM users WHERE id = '{user_from_token['id']}' AND email = '{user_from_token['email']}' AND password = '{user_from_token['password']}'")

        result = cursor.fetchone()

        if not result:
            return None

        user = { 'id': result[0], 'name': result[1], 'email': result[2], 'password': result[3], 'role': result[4] }

        cursor.close()
        self.__connection.close()

        return user

    def get_id_by_token(self, token: str):
        return decode_token(token)['sub']['id']

    def get_user_name_by_id(self, id: int) -> str:
        self.__connection = get_connection()
        cursor = self.__connection.cursor()

        cursor.execute(f"SELECT name FROM users WHERE id = {id}")

        result = cursor.fetchone()

        if not result:
            return ''

        cursor.close()
        self.__connection.close()

        return result[0]
