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

    # Erstelle ein Cursor-Objekt
    cur = connection.cursor()

    isReadyToMigrate = False

    for table in tables:
        # SQL-Abfrage zum Überprüfen, ob die Tabelle existiert
        query ="""
            SELECT EXISTS (
                SELECT 1
                FROM information_schema.tables 
                WHERE table_name = %s
            );
        """

        # Führe die Abfrage aus
        cur.execute(query, (table,))
        result = cur.fetchone()

        # Prüfe, ob die Tabelle existiert
        if result[0]:
            isReadyToMigrate = False
        else:
            isReadyToMigrate = True
            break

        # Schließe den Cursor
    cur.close()
    return isReadyToMigrate