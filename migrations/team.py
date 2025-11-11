from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate team data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "team")
    for row in data:
        team_id = row[0]
        name = row[1]
        access_code = row[2]
        created_at = row[3]
        updated_at = row[4]
        deleted_at = row[5]
        logo_url = row[6]

        postgres_cursor.execute("""
            INSERT INTO team (
                team_id, name, access_code, created_at,
                updated_at, deleted_at, logo_url
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            team_id, name, access_code, created_at,
            updated_at, deleted_at, logo_url
        ))
        
    postgres_cursor.connection.commit()