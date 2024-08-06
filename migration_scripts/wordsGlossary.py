from datetime import datetime
import pytz
from BColors import BColors

def migrate_words_glossary(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating words glossary...{BColors.ENDC}")
    words_glossary_id_map = {}
    org_id_map = kwargs["org_id_map"]
    for document in cursor:
        mongo_id = document.get("_id")
        name = document.get("name")
        description = document.get("description")
        points = document.get("points")
        example = document.get("example")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        organizationId = document.get("OrganizationId")
        
        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = createdAt or current_time
            updatedAt = updatedAt or current_time

        # Only migrate if the organizationId is in the org_id_map
        if str(organizationId) in org_id_map:
            org_id_to_assign = org_id_map[str(organizationId)]
            
            # Insert the wordsGlossary record into the database
            insert_query = 'INSERT INTO public."WordsGlossary" ("name", "description", "points", "example", "organizationId", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (name, description, points, example, org_id_to_assign, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            words_glossary_id_map[str(mongo_id)] = new_id

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return words_glossary_id_map
