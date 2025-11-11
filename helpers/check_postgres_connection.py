import psycopg2
from psycopg2 import OperationalError

def check_postgres_connection(host, dbname, user, password):
    try:
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        connection.close()
    
    except OperationalError as e:
        return False
    
    return True
