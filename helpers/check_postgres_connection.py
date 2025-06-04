import psycopg2
from psycopg2 import OperationalError

def check_postgres_connection(host, dbname, user, password):
    try:
        # Versuche eine Verbindung zur Datenbank herzustellen
        connection = psycopg2.connect(
            host=host,
            dbname=dbname,
            user=user,
            password=password
        )
        # Wenn die Verbindung erfolgreich ist
        print("✅ Connection to PostgreSQL is successful.")
        
        # Schließe die Verbindung, falls sie erfolgreich war
        connection.close()
    
    except OperationalError as e:
        # Falls die Verbindung fehlschlägt
        print(f"Error: Unable to connect to the database. {e}")
        return False
    
    return True
