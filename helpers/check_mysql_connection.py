import mysql.connector
from mysql.connector import Error

def check_mysql_connection(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host=host,
            database=database,
            user=user,
            password=password
        )
        
        if connection.is_connected():
            print("✅ Connection to MySQL is successful.")
            connection.close()
            return True
        else:
            print("Connection to MySQL failed.")
            return False
    
    except Error as e:
        print(f"Error: Unable to connect to the MySQL database. {e}")
        return False