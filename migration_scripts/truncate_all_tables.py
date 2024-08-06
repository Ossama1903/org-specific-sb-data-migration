import psycopg2
from connections import postgres_connection
from BColors import BColors


def truncate_all_tables():
    """
    Truncate all tables in the 'public' schema of the PostgreSQL database,
    resetting their identity columns and cascading deletions.
    """
    try:
        print(f"{BColors.WARNING}Truncating tables...{BColors.ENDC}")
        with  postgres_connection() as postgres_conn:
        # Connect to the database
            postgres_conn.autocommit = True  # Ensure changes are committed immediately
            cur = postgres_conn.cursor()

            # SQL command to truncate all tables
            truncate_command = """
            DO $$
            DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public')
                LOOP
                    EXECUTE 'TRUNCATE TABLE public.' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE;';
                END LOOP;
            END $$;
            """

            # Execute the command
            cur.execute(truncate_command)
            print(f"{BColors.OKGREEN}All tables have been successfully truncated.{BColors.ENDC}")

    except psycopg2.Error as e:
        print(f"An error occurred while truncating tables: {e}")
    finally:
        # Close the cursor and connection
        if cur is not None:
            cur.close()
        if postgres_conn is not None:
            postgres_conn.close()

# Example usage:
# db_connection_string = "dbname=test user=postgres password=secret host=localhost"
# truncate_all_tables(db_connection_string)
