from psycopg2 import connect
from os import environ
from sqlalchemy import create_engine
def get_connection():

    if environ.get("DB_ENV") == "local":
        print("local env")
        return connect(
            dbname=environ.get("DB_NAME"),
            user=environ.get("DB_USER"),
            password=environ.get("DB_PASSWORD"),
            host=environ.get("DB_HOST"),
            port=environ.get("DB_PORT")
        )
    elif environ.get("DB_ENV") == "remote":
        print("Remote")

        db_user = environ.get('DB_USER_REMOTE')
        db_password = environ.get('DB_PASSWORD_REMOTE')
        db_host = environ.get('DB_HOST_REMOTE')
        db_port = environ.get('DB_PORT_REMOTE', '5432')  # Default to port 5432 if not set
        db_name = environ.get('DB_NAME_REMOTE')

        if not all([db_user, db_password, db_host, db_name]):
            raise ValueError('Missing required environment variables for database connection')

        db_uri = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

        return connect(db_uri)
