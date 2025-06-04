from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate user data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "user")
    for row in data:
        user_id = row[0]
        username = row[1]
        password = row[2]
        role = row[3]
        created_at = row[4]
        updated_at = row[5]
        deleted_at = row[6]
        display_name = row[7]
        logo_url = row[8]

        postgres_cursor.execute("""
            INSERT INTO "user" (
                user_id, username, password, role, created_at,
                updated_at, deleted_at, display_name, logo_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            user_id, username, password, role,
            created_at, updated_at, deleted_at,
            display_name, logo_url
        ))
    
    postgres_cursor.connection.commit()