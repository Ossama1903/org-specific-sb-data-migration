from datetime import datetime
import pytz
from BColors import BColors

def migrate_lessons(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating lessons...{BColors.ENDC}")
    lesson_id_map = {}
    module_id_map = kwargs["module_id_map"]
    icon_id_map = kwargs["icon_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        description = document.get("description")
        status = document.get("status")
        priorityIndex = document.get("priorityIndex")
        moduleID = str(document.get("moduleID"))
        iconID = str(document.get("iconID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the moduleID and iconID exist in the corresponding maps
        if moduleID in module_id_map and iconID in icon_id_map:
            postgres_module_id = module_id_map[moduleID]
            postgres_icon_id = icon_id_map[iconID]

            # Insert the lesson record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Lesson" ("name", "description", "status", "priorityIndex", "moduleId", "iconId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, description, status, priorityIndex, postgres_module_id, postgres_icon_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            lesson_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if moduleID not in module_id_map:
                missing_ids.append(f"moduleID {moduleID}")
            if iconID not in icon_id_map:
                missing_ids.append(f"iconID {iconID}")
            print(f"{BColors.FAIL}Skipping lesson {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Lessons migration completed{BColors.ENDC}")
    return lesson_id_map
