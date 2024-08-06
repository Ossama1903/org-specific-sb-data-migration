from datetime import datetime
import pytz
from BColors import BColors

def migrate_promptcategories(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating prompt categories...{BColors.ENDC}")
    promptcategory_id_map = {}

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Insert the prompt category record into the PostgreSQL database
        insert_query = '''
        INSERT INTO public."PromptCategory" ("name", "createdAt", "updatedAt")
        VALUES (%s, %s, %s) RETURNING id
        '''
        data = (name, createdAt, updatedAt)
        postgres_cursor.execute(insert_query, data)
        new_id = postgres_cursor.fetchone()[0]
        promptcategory_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}Prompt categories migration completed{BColors.ENDC}")
    return promptcategory_id_map
