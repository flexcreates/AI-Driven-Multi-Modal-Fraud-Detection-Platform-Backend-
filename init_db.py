import os
import psycopg2
from psycopg2 import sql
from SRC.config.settings import settings

def init_db():
    # Connect to default 'postgres' database to check/create the target DB
    conn = psycopg2.connect(
        user=settings.POSTGRES_USER,
        password=settings.POSTGRES_PASSWORD,
        host=settings.POSTGRES_SERVER,
        port=settings.POSTGRES_PORT,
        dbname="postgres"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Check if database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.POSTGRES_DB}'")
    exists = cursor.fetchone()
    
    if not exists:
        print(f"Creating database {settings.POSTGRES_DB}...")
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(
            sql.Identifier(settings.POSTGRES_DB)
        ))
    else:
        print(f"Database {settings.POSTGRES_DB} already exists.")
    
    cursor.close()
    conn.close()

    # Now connect to the target database and run schema/seed
    print(f"Connecting to {settings.POSTGRES_DB} on {settings.POSTGRES_SERVER}...")
    try:
        # Try connecting with explicit parameters first to rule out URL issues
        conn = psycopg2.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_SERVER,
            port=settings.POSTGRES_PORT,
            dbname=settings.POSTGRES_DB
        )
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("Running schema.sql...")
        with open("DATABASE/schema.sql", "r") as f:
            cursor.execute(f.read())
            
        print("Running seed_data.sql...")
        try:
            with open("DATABASE/seed_data.sql", "r") as f:
                cursor.execute(f.read())
        except psycopg2.errors.UniqueViolation:
            print("Seed data might already exist, skipping.")
        except Exception as e:
            print(f"Error seeding data: {e}")

        cursor.close()
        conn.close()
        print("Database initialization complete.")
        
    except Exception as e:
        print(f"Failed to connect to target database: {e}")
        print(f"Debug info: User={settings.POSTGRES_USER}, Host={settings.POSTGRES_SERVER}, DB={settings.POSTGRES_DB}")
        raise e

if __name__ == "__main__":
    init_db()
