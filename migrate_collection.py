from connections import mongo_connection, postgres_connection


def migrate_collection(collection_name, migrate_function, **kwargs):
    """General function to migrate data for a specified collection."""
    with mongo_connection() as mongodb, postgres_connection() as postgres_conn:
        collection = mongodb[collection_name]
        cursor = collection.find()
        postgres_cursor = postgres_conn.cursor()
        try:
            return migrate_function(cursor, postgres_cursor, **kwargs)
        finally:
            postgres_cursor.close()
