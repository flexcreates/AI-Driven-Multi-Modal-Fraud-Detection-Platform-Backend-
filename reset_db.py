import psycopg2
from psycopg2 import sql
from SRC.config.settings import settings
import sys
import init_db

def reset_db(confirm=False):
    print("WARNING: This will DROP the entire database and lose all data.")
    if not confirm:
        user_input = input("Are you sure? (y/n): ")
        if user_input.lower() != 'y':
            print("Aborted.")
            return

    # Connect to default 'postgres' database to drop the target DB
    try:
        conn = psycopg2.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            dbname="postgres"
        )
        conn.autocommit = True
        cursor = conn.cursor()

        # Terminate existing connections
        print(f"Terminating connections to {settings.POSTGRES_DB}...")
        cursor.execute(sql.SQL("""
            SELECT pg_terminate_backend(pg_stat_activity.pid)
            FROM pg_stat_activity
            WHERE pg_stat_activity.datname = {}
            AND pid <> pg_backend_pid();
        """).format(sql.Literal(settings.POSTGRES_DB)))

        # Drop Database
        print(f"Dropping database {settings.POSTGRES_DB}...")
        cursor.execute(sql.SQL("DROP DATABASE IF EXISTS {}").format(
            sql.Identifier(settings.POSTGRES_DB)
        ))
        
        cursor.close()
        conn.close()
        print("Database dropped.")

        # Re-initialize
        print("Re-initializing database...")
        init_db.init_db()
        
    except Exception as e:
        print(f"Error resetting database: {e}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        reset_db(confirm=True)
    else:
        reset_db()
