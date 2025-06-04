from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate session data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "session_data")
    for row in data:
        session_data_id = row[0]
        website_id = row[1]
        session_id = row[2]
        data_key = row[3]
        string_value = row[4]
        number_value = row[5]
        date_value = row[6]
        data_type = row[7]
        created_at = row[8]
        distinct_id = row[9]

        postgres_cursor.execute("""
            INSERT INTO session_data (
                session_data_id, website_id, session_id, data_key, string_value,
                number_value, date_value, data_type, created_at, distinct_id
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            session_data_id, website_id, session_id, data_key, string_value,
            number_value, date_value, data_type, created_at, distinct_id
        ))

    
    postgres_cursor.connection.commit()