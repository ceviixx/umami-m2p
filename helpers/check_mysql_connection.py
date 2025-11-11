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
            connection.close()
            return True
        else:
            return False
    
    except Error as e:
        return False