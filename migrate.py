import helpers.check_setup
import helpers.create_tables
import migrations._prisma_migrations
import migrations.event_data
import migrations.report
import migrations.revenue
import migrations.segment
import migrations.session
import migrations.session_data
import migrations.team
import migrations.team_user
import migrations.user
import migrations.website
import migrations.website_event
import mysql.connector
import psycopg2
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


print("\n" + "="*70)
print("  🚀 UMAMI MIGRATION: MySQL → PostgreSQL")
print("="*70 + "\n")

# Check MySQL connection
mysql_connection_ok = check_mysql_connection(
    host=mysql_host,
    database=mysql_database,
    user=mysql_user,
    password=mysql_password
)

if mysql_connection_ok:
    print(f"✅ MySQL")
else:
    print(f"❌ MySQL ({mysql_host}:{mysql_port}/{mysql_database})")
    print("   → Check if server is running and credentials are correct")

# Check PostgreSQL connection
postgres_connection_ok = check_postgres_connection(
    host=postgres_host,
    dbname=postgres_database,
    user=postgres_user,
    password=postgres_password
)

if postgres_connection_ok:
    print(f"✅ PostgreSQL")
else:
    print(f"❌ PostgreSQL ({postgres_host}:{postgres_port}/{postgres_database})")
    print("   → Check if server is running and credentials are correct")

# Exit if any connection failed
if not mysql_connection_ok or not postgres_connection_ok:
    print("\n" + "="*70)
    exit(1)

print("")



# Setup connections for migration
try:
    mysql_conn = mysql.connector.connect(
        host=mysql_host,
        user=mysql_user,
        password=mysql_password,
        database=mysql_database,
        port=mysql_port,
    )
except Exception as e:
    print(f"\n❌ Failed to establish MySQL connection: {str(e)}")
    exit(1)

try:
    postgres_conn = psycopg2.connect(
        host=postgres_host,
        user=postgres_user,
        password=postgres_password,
        database=postgres_database,
        port=postgres_port,
    )
except Exception as e:
    print(f"\n❌ Failed to establish PostgreSQL connection: {str(e)}")
    mysql_conn.close()
    exit(1)



mysql_cur = mysql_conn.cursor()
postgres_cur = postgres_conn.cursor()

print("🔍 Checking source tables...", end='', flush=True)

# Get all tables from MySQL source
mysql_cur.execute("SHOW TABLES")
source_tables = [row[0] for row in mysql_cur.fetchall()]

print(f" ✅ ({len(source_tables)} found)")

# Check if PostgreSQL is ready for migration
print("🔍 Checking target database...", end='', flush=True)
isReadyToMigrate = check_setup(postgres_conn)

if isReadyToMigrate == False:
    print(" ❌\n")
    print("="*70)
    print("  ❌ Database already contains Umami tables")
    print("="*70)
    print("\n  Options:")
    print("    1. Drop existing tables")
    print("    2. Use a different database")
    print("\n" + "="*70)
    mysql_cur.close()
    postgres_cur.close()
    mysql_conn.close()
    postgres_conn.close()
    exit(1)

print(" ✅\n")

print("="*70)
print("  🎯 TRANSACTION-BASED MIGRATION")
print("="*70)
print("  All changes in one transaction - rollback on error")
print("="*70 + "\n")

input("Press Enter to start migration...")

# Define all possible migrations with their table names
# IMPORTANT: Order matters due to foreign key dependencies!
all_migrations = [
    ("_prisma_migrations", "Prisma migrations", migrations._prisma_migrations.migrate, helpers.create_tables.create_prisma_migrations_table),
    ("user", "Users", migrations.user.migrate, helpers.create_tables.create_user_table),
    ("team", "Teams", migrations.team.migrate, helpers.create_tables.create_team_table),
    ("team_user", "Team users", migrations.team_user.migrate, helpers.create_tables.create_team_user_table),
    ("website", "Websites", migrations.website.migrate, helpers.create_tables.create_website_table),
    ("session", "Sessions", migrations.session.migrate, helpers.create_tables.create_session_table),
    ("revenue", "Revenue", migrations.revenue.migrate, helpers.create_tables.create_revenue_table),
    ("website_event", "Website events", migrations.website_event.migrate, helpers.create_tables.create_website_event_table),
    ("event_data", "Event data", migrations.event_data.migrate, helpers.create_tables.create_event_data_table),
    ("session_data", "Session data", migrations.session_data.migrate, helpers.create_tables.create_session_data_table),
    ("report", "Reports", migrations.report.migrate, helpers.create_tables.create_report_table),
    ("segment", "Segments", migrations.segment.migrate, helpers.create_tables.create_segment_table),
]

# Filter migrations based on source tables
migrations_to_run = [(table, label, migrate_func, create_func) 
                     for table, label, migrate_func, create_func in all_migrations 
                     if table in source_tables]

skipped_tables = [table for table, _, _, _ in all_migrations if table not in source_tables]

if skipped_tables:
    print(f"\nℹ️  Skipping {len(skipped_tables)} tables not in source:")
    for table in skipped_tables:
        print(f"   • {table}")
    print()

print(f"📦 Migrating {len(migrations_to_run)} tables...\n")

try:
    print("🏗️  Creating tables...")
    
    # Create only tables that exist in source
    for table_name, label, _, create_func in migrations_to_run:
        print(f"  • {label}...", end='', flush=True)
        create_func(postgres_cur)
        print(" ✅")
    
    print("\n📥 Copying data...")
    
    # Migrate only tables that exist in source
    for table_name, label, migrate_func, _ in migrations_to_run:
        print(f"  • {label}...", end='', flush=True)
        migrate_func(mysql_cur, postgres_cur)
        print(" ✅")

    # Validation: Compare row counts
    print("\n🔍 Validating migration...")
    print("="*70)
    
    validation_passed = True
    max_label_length = max(len(label) for _, label, _, _ in migrations_to_run)
    
    for table_name, label, _, _ in migrations_to_run:
        # Get MySQL count
        mysql_cur.execute(f"SELECT COUNT(*) FROM `{table_name}`")
        mysql_count = mysql_cur.fetchone()[0]
        
        # Get PostgreSQL count
        postgres_cur.execute(f'SELECT COUNT(*) FROM "{table_name}"')
        postgres_count = postgres_cur.fetchone()[0]
        
        # Format output
        match_symbol = "✅" if mysql_count == postgres_count else "❌"
        label_padded = label.ljust(max_label_length)
        
        print(f"  {match_symbol} {label_padded}  MySQL: {mysql_count:>6}  →  PostgreSQL: {postgres_count:>6}")
        
        if mysql_count != postgres_count:
            validation_passed = False
    
    print("="*70)
    
    if validation_passed:
        print("  ✅ VALIDATION PASSED - All row counts match")
    else:
        print("  ⚠️  WARNING - Row count mismatch detected")
    
    print("="*70 + "\n")
    
    # Ask for confirmation before committing
    finalize = input("Migration prepared successfully - finalize? (y/N): ").strip().lower()
    
    if finalize == 'y':
        print("\n💾 Committing...", end='', flush=True)
        try:
            postgres_conn.commit()
            print(" ✅\n")
            print("="*70)
            print("  ✅ MIGRATION COMPLETED")
            print("="*70 + "\n")
        except Exception as commit_error:
            print(" ❌\n")
            print("="*70)
            print("  ❌ COMMIT FAILED")
            print("="*70)
            print(f"  Error: {str(commit_error)}")
            print("\n  Rolling back...", end='', flush=True)
            try:
                postgres_conn.rollback()
                print(" ✅")
                print("  Database unchanged\n")
            except:
                print(" ❌\n")
            print("="*70)
            
            # Close connections
            postgres_cur.close()
            mysql_cur.close()
            postgres_conn.close()
            mysql_conn.close()
            exit(1)
    else:
        print("\n🔄 Rolling back...", end='', flush=True)
        postgres_conn.rollback()
        print(" ✅")
        print("\n" + "="*70)
        print("  ℹ️  MIGRATION CANCELLED - Database unchanged")
        print("="*70 + "\n")
        
        # Close connections
        postgres_cur.close()
        mysql_cur.close()
        postgres_conn.close()
        mysql_conn.close()
        exit(0)

except Exception as e:
    print(" ❌\n")
    print("="*70)
    print("  ❌ MIGRATION FAILED")
    print("="*70)
    print(f"  Error: {str(e)}")
    print(f"  Type:  {type(e).__name__}")
    print("\n  Rolling back...", end='', flush=True)
    
    # On error, everything is rolled back
    try:
        postgres_conn.rollback()
        print(" ✅")
        print("  Database unchanged\n")
    except Exception as rollback_error:
        print(f" ❌\n")
        print(f"  Rollback error: {str(rollback_error)}\n")
    
    print("="*70)
    
    # Close connections
    try:
        postgres_cur.close()
        mysql_cur.close()
        postgres_conn.close()
        mysql_conn.close()
    except:
        pass
    
    exit(1)


# Close the database connections
postgres_cur.close()
mysql_cur.close()
postgres_conn.close()
mysql_conn.close()
