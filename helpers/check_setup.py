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

    cur = connection.cursor()

    isReadyToMigrate = False

    for table in tables:
        query ="""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """

        cur.execute(query, (table,))
        result = cur.fetchone()

        if result[0]:
            isReadyToMigrate = False
        else:
            isReadyToMigrate = True
            break

    cur.close()
    return isReadyToMigrate