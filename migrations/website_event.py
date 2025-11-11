from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate website event data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "website_event")
    for row in data:
        event_id = row[0]
        website_id = row[1]
        session_id = row[2]
        created_at = row[3]
        url_path = row[4]
        url_query = row[5]
        referrer_path = row[6]
        referrer_query = row[7]
        referrer_domain = row[8]
        page_title = row[9]
        event_type = row[10]
        event_name = row[11]
        visit_id = row[12]
        tag = row[13]
        fbclid = row[14]
        gclid = row[15]
        li_fat_id = row[16]
        msclkid = row[17]
        ttclid = row[18]
        twclid = row[19]
        utm_campaign = row[20]
        utm_content = row[21]
        utm_medium = row[22]
        utm_source = row[23]
        utm_term = row[24]
        hostname = row[25]

        postgres_cursor.execute(
            """
            INSERT INTO website_event (
                id, website_id, session_id, created_at, url_path, url_query,
                referrer_path, referrer_query, referrer_domain, page_title,
                event_type, event_name, visit_id, tag, fbclid, gclid,
                li_fat_id, msclkid, ttclid, twclid, utm_campaign,
                utm_content, utm_medium, utm_source, utm_term,
                hostname
            ) VALUES (
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s, %s, %s, %s,
                %s
            )
            """,
            (
                event_id,
                website_id,
                session_id,
                created_at,
                url_path,
                url_query,
                referrer_path,
                referrer_query,
                referrer_domain,
                page_title,
                event_type,
                event_name,
                visit_id,
                tag,
                fbclid,
                gclid,
                li_fat_id,
                msclkid,
                ttclid,
                twclid,
                utm_campaign,
                utm_content,
                utm_medium,
                utm_source,
                utm_term,
                hostname
            )
        )
        
    postgres_cursor.connection.commit()