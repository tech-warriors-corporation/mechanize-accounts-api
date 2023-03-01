from database import get_connection

class UserRepository:
    def __init__(self):
        self.connection = None

    def create(self, name: str, email: str, password: str, role: str):
        self.connection = get_connection()
        cursor = self.connection.cursor()

        cursor.execute(f"INSERT INTO users (name, email, password, role) VALUES ('{name}', '{email}', '{password}', '{role}')")
        self.connection.commit()
        cursor.close()
        self.connection.close()
