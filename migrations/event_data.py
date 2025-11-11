from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate event data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "event_data")
    for row in data:
        event_data_id = row[0]
        website_event_id = row[1]
        website_id = row[2]
        data_key = row[3]
        string_value = row[4]
        number_value = row[5]
        date_value = row[6]
        data_type = row[7]
        created_at = row[8]

        postgres_cursor.execute("""
            INSERT INTO event_data (
                event_data_id,
                website_event_id,
                website_id,
                data_key,
                string_value,
                number_value,
                date_value,
                data_type,
                created_at
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            event_data_id,
            website_event_id,
            website_id,
            data_key,
            string_value,
            number_value,
            date_value,
            data_type,
            created_at
        ))
        
    postgres_cursor.connection.commit()