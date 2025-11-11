from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate revenue data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "revenue")
    for row in data:
        revenue_id = row[0]
        website_id = row[1]
        session_id = row[2]
        event_id = row[3]
        event_name = row[4]
        currency = row[5]
        revenue = row[6]
        created_at = row[7]

        postgres_cursor.execute("""
            INSERT INTO revenue (
                revenue_id, website_id, session_id, event_id,
                event_name, currency, revenue, created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            revenue_id, website_id, session_id, event_id,
            event_name, currency, revenue, created_at
        ))
    
    # Commit happens at the end of the entire migration
