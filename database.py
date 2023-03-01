from psycopg2 import connect
from os import environ

def get_connection():
    return connect(
        dbname=environ.get("DB_NAME"),
        user=environ.get("DB_USER"),
        password=environ.get("DB_PASSWORD"),
        host=environ.get("DB_HOST"),
        port=environ.get("DB_PORT")
    )
