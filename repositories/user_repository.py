from database import get_connection

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
