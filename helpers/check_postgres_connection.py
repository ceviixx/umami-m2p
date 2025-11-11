import psycopg2
from psycopg2 import OperationalError

def check_postgres_connection(host, dbname, user, password):
    try:
        # Try to establish a connection to the database
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        # If the connection is successful
        print("✅ Connection to PostgreSQL is successful.")
        
        # Close the connection if it was successful
        connection.close()
    
    except OperationalError as e:
        # If the connection fails
        print(f"Error: Unable to connect to the database. {e}")
        return False
    
    return True
