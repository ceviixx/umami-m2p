from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate segment data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "segment")
    for row in data:
        segment_id = row[0]
        website_id = row[1]
        type = row[2]
        name = row[3]
        parameters = row[4]
        created_at = row[5]
        updated_at = row[6]

        postgres_cursor.execute("""
            INSERT INTO segment (
                segment_id, website_id, type, name,
                parameters, created_at, updated_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (
            segment_id, website_id, type, name,
            parameters, created_at, updated_at
        ))
    
    # Commit happens at the end of the entire migration
