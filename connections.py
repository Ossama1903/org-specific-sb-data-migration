import pymongo
import psycopg2
import config
from contextlib import contextmanager

@contextmanager
def mongo_connection():
    """Context manager for MongoDB connection."""
    mongo_client = pymongo.MongoClient(config.MONGODB_CONNECTION_STRING)
    try:
        yield mongo_client[config.MONGODB_DATABASE_NAME]
    finally:
        mongo_client.close()

@contextmanager
def postgres_connection():
    """Context manager for PostgreSQL connection."""
    conn = psycopg2.connect(config.POSTGRES_CONNECTION_STRING)
    try:
        yield conn
        print("PostgreSQL: Connected")
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"PostgreSQL: Connection failed - {e}")
        raise e
    finally:
        conn.close()