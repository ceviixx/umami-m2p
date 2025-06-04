import helpers.check_setup
import helpers.create_tables
import migrations._prisma_migrations
import migrations.event_data
import migrations.report
import migrations.session
import migrations.session_data
import migrations.team
import migrations.team_user
import migrations.user
import migrations.website
import migrations.website_event
import mysql.connector
import psycopg2
import time
from dotenv import load_dotenv
import os

# Import helper functions
from helpers.check_postgres_connection import check_postgres_connection
from helpers.check_mysql_connection import check_mysql_connection
from helpers.check_setup import check_setup
import helpers

# Import migration functions
import migrations


load_dotenv()

## Define your database connection parameters
# MySQL connection parameters
mysql_host = os.getenv("MYSQL_HOST")
mysql_database = os.getenv("MYSQL_DATABASE")
mysql_user = os.getenv("MYSQL_USER")
mysql_password = os.getenv("MYSQL_PASSWORD")
mysql_port = os.getenv("MYSQL_PORT", 3306)
# PostgreSQL connection parameters
postgres_host = os.getenv("POSTGRES_HOST")
postgres_database = os.getenv("POSTGRES_DATABASE")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")
postgres_port = os.getenv("POSTGRES_PORT", 5432)



# Check MySQL connection
mysql_connection_ok = check_mysql_connection(
    host=mysql_host,
    database=mysql_database,
    user=mysql_user,
    password=mysql_password
)

# Check PostgreSQL connection
postgres_connection_ok = check_postgres_connection(
    host=postgres_host,
    dbname=postgres_database,
    user=postgres_user,
    password=postgres_password
)


if not mysql_connection_ok and not postgres_connection_ok:
    print("❌ Exit migration, no database connection possible.")
    exit(1)


# Setup connections for migration
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="umami",
    password="umami",
    database="umami",
    port=3306,
)

postgres_conn = psycopg2.connect(
    host="localhost",
    user="clemensschafer",
    password="umami",
    database="umami_dev",
    port=5432,
)


mysql_cur = mysql_conn.cursor()
postgres_cur = postgres_conn.cursor()


print("🔄 Check if umami already setup...")
isReadyToMigrate = check_setup(postgres_conn)

if isReadyToMigrate == False:
    print("\n\n")
    print("❌ You have already setup Umami in your PostgreSQL database.")
    print("Please remove the existing tables in your PostgreSQL database or use a different database.")
    print("Exiting migration...")
    print("\n\n")
    mysql_cur.close()
    postgres_cur.close()
    exit(1)

print("✅ Umami is setup, starting migration...")

input("Press Enter to create relevant tables...", end='', flush=True)
helpers.create_tables.create_tables_and_indexes(postgres_cur)
print(" ✅")


print("\n\n")

input("Press Enter to start the migration...")

print("Migrating Prisma migrations...", end='', flush=True)
time.sleep(1)
migrations._prisma_migrations.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating users...", end='', flush=True)
time.sleep(1)
migrations.user.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating team...", end='', flush=True)
time.sleep(1)
migrations.team.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating team user...", end='', flush=True)
time.sleep(1)
migrations.team_user.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating website...", end='', flush=True)
time.sleep(1)
migrations.website.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating website event...", end='', flush=True)
time.sleep(1)
migrations.website_event.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating event data...", end='', flush=True)
time.sleep(1)
migrations.event_data.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating session...", end='', flush=True)
time.sleep(1)
migrations.session.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating session data...", end='', flush=True)
time.sleep(1)
migrations.session_data.migrate(mysql_cur, postgres_cur)
print(" ✅")

print("Migrating report...", end='', flush=True)
time.sleep(1)
migrations.report.migrate(mysql_cur, postgres_cur)
print(" ✅")


print("✅ Migration completed successfully!")
print("Please check the data in your PostgreSQL database to ensure everything is correct.")


# Close the database connections
postgres_cur.close()
mysql_cur.close()

