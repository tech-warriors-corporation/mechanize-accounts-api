from database import get_connection

class UserRepository:
    def __init__(self):
        self.__connection = None

    def create(self, name: str, email: str, password: str, role: str):
        self.__connection = get_connection()
        cursor = self.__connection.cursor()

        cursor.execute(f"INSERT INTO users (name, email, password, role) VALUES ('{name}', '{email}', '{password}', '{role}')")
        self.__connection.commit()
        cursor.close()
        self.__connection.close()
