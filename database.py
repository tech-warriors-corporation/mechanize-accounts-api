from psycopg2 import connect
from os import environ

def get_connection():
    is_local = environ.get("DB_ENV") == "local"
    db_name = environ.get("DB_NAME") if is_local else environ.get('DB_NAME_REMOTE')
    user = environ.get("DB_USER") if is_local else environ.get('DB_USER_REMOTE')
    password = environ.get("DB_PASSWORD") if is_local else environ.get('DB_PASSWORD_REMOTE')
    host = environ.get("DB_HOST") if is_local else environ.get('DB_HOST_REMOTE')
    port = environ.get("DB_PORT") if is_local else environ.get('DB_PORT_REMOTE')

    if not all([db_name, user, password, host, port]):
        raise ValueError('Missing required environment variables for database connection!')

    return connect(
        dbname=db_name,
        user=user,
        password=password,
        host=host,
        port=port
    )
