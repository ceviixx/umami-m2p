from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate session from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "session")
    for row in data:
        session_id = row[0]
        website_id = row[1]
        browser = row[2]
        os = row[3]
        device = row[4]
        screen = row[5]
        language = row[6]
        country = row[7]
        region = row[8]
        city = row[9]
        created_at = row[10]
        distinct_id = row[11]

        postgres_cursor.execute("""
            INSERT INTO session (
                id, website_id, browser, os, device, screen, language,
                country, region, city, created_at, distinct_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session_id, website_id, browser, os, device, screen, language,
            country, region, city, created_at, distinct_id
        ))
    
    postgres_cursor.connection.commit()