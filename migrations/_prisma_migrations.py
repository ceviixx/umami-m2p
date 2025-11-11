from helpers.fetch_data import fetch_data

def migrate(mysql_cursor, postgres_cursor):
    """
    Migrate prisma data from MySQL to PostgreSQL.
    """

    data = fetch_data(mysql_cursor, "_prisma_migrations")
    for row in data:
        id = row[0]
        checksum = row[1]
        finished_at = row[2]
        migration_name = row[3]
        logs = row[4]
        rolled_back_at = row[5]
        started_at = row[6]
        applied_steps_count = row[7]

        postgres_cursor.execute("""
            INSERT INTO "_prisma_migrations" (
                "id", "checksum", "finished_at", "migration_name",
                "logs", "rolled_back_at", "started_at", "applied_steps_count"
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (id, checksum, finished_at, migration_name, logs, rolled_back_at, started_at, applied_steps_count))
    
    postgres_cursor.connection.commit()