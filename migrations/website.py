from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate website data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "website")
    for row in data:
        website_id = row[0]
        name = row[1]
        domain = row[2]
        share_id = row[3]
        reset_at = row[4]
        user_id = row[5]
        created_at = row[6]
        updated_at = row[7]
        deleted_at = row[8]
        created_by = row[9]
        team_id = row[10]

        postgres_cursor.execute("""
            INSERT INTO website (
                website_id, name, domain, share_id, reset_at, user_id,
                created_at, updated_at, deleted_at, created_by, team_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            website_id, name, domain, share_id, reset_at,
            user_id, created_at, updated_at, deleted_at,
            created_by, team_id
        ))
    
    postgres_cursor.connection.commit()