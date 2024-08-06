from datetime import datetime
import pytz
from BColors import BColors

def migrate_prompts(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating prompts...{BColors.ENDC}")
    prompt_id_map = {}
    promptcategory_id_map = kwargs["promptcategory_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        content = document.get("content")
        category = str(document.get("category"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the category exists in the corresponding map
        if category in promptcategory_id_map:
            postgres_category_id = promptcategory_id_map[category]

            # Insert the prompt record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Prompt" ("name", "content", "categoryId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, content, postgres_category_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            prompt_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping prompt {mongo_id} due to missing category {category}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Prompts migration completed{BColors.ENDC}")
    return prompt_id_map
