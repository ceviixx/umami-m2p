def check_setup(connection):

    tables = [
        '_prisma_migrations',
        'event_data',
        'report',
        'session',
        'session_data',
        'team',
        'team_user',
        'user',
        'website',
        'website_event'
    ]

    # Create a cursor object
    cur = connection.cursor()

    isReadyToMigrate = False

    for table in tables:
        # SQL query to check if the table exists
        query ="""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """

        # Execute the query
        cur.execute(query, (table,))
        result = cur.fetchone()

        # Check if the table exists
        if result[0]:
            isReadyToMigrate = False
        else:
            isReadyToMigrate = True
            break

        # Close the cursor
    cur.close()
    return isReadyToMigrate