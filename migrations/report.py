from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate report from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "report")
    for row in data:
        report_id = row[0]
        user_id = row[1]
        website_id = row[2]
        type = row[3]
        name = row[4]
        description = row[5]
        parameters = row[6]
        created_at = row[7]
        updated_at = row[8]
    
        postgres_cursor.execute("""
            INSERT INTO report (report_id, user_id, website_id, type, name, description, parameters, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (report_id, user_id, website_id, type, name, description, parameters, created_at, updated_at))
        
    
    postgres_cursor.connection.commit()