from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate team user data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "team_user")
    for row in data:
        team_user_id = row[0]
        team_id = row[1]
        user_id = row[2]
        role = row[3]
        created_at = row[4]
        updated_at = row[5]

        postgres_cursor.execute("""
            INSERT INTO team_user (team_user_id, team_id, user_id, role, created_at, updated_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (team_user_id) DO UPDATE
            SET team_id = EXCLUDED.team_id,
                user_id = EXCLUDED.user_id,
                role = EXCLUDED.role,
                created_at = EXCLUDED.created_at,
                updated_at = EXCLUDED.updated_at;
        """, (team_user_id, team_id, user_id, role, created_at, updated_at))
        
    postgres_cursor.connection.commit()
