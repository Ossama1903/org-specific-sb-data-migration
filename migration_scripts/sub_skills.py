from datetime import datetime
import pytz
from BColors import BColors

def migrate_subskills(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating subskills...{BColors.ENDC}")
    subskill_id_map = {}
    skill_id_map = kwargs["skill_id_map"]
    icon_id_map = kwargs["icon_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        description = document.get("description")
        status = document.get("status")
        priorityIndex = document.get("priorityIndex")
        skillID = str(document.get("skillID"))
        iconID = str(document.get("iconID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the skillID and iconID exist in the corresponding maps
        if skillID in skill_id_map:
            postgres_skill_id = skill_id_map[skillID]
            postgres_icon_id = None
            if iconID in icon_id_map:
                postgres_icon_id = icon_id_map[iconID]

            # Insert the subskill record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."SubSkill" ("name", "description", "status", "priorityIndex", "skillId", "iconId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, description, status, priorityIndex, postgres_skill_id, postgres_icon_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            subskill_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if skillID not in skill_id_map:
                missing_ids.append(f"skillID {skillID}")
            print(f"{BColors.FAIL}Skipping subskill {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Subskills migration completed{BColors.ENDC}")
    return subskill_id_map
