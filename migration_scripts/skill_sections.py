from datetime import datetime
import pytz
from BColors import BColors

def migrate_skillsections(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating skill sections...{BColors.ENDC}")
    skillsection_id_map = {}
    subskill_id_map = kwargs["subskill_id_map"]
    allcontent_id_map = kwargs["allcontent_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        priorityIndex = document.get("priorityIndex")
        subSkillID = str(document.get("subSkillID"))
        allContentID = str(document.get("allContentID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the subSkillID and allContentID exist in the corresponding maps
        if subSkillID in subskill_id_map and allContentID in allcontent_id_map:
            postgres_subskill_id = subskill_id_map[subSkillID]
            postgres_allcontent_id = allcontent_id_map[allContentID]

            # Insert the skill section record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."SkillSection" ("name", "priorityIndex", "subSkillId", "allContentId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, priorityIndex, postgres_subskill_id, postgres_allcontent_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            skillsection_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if subSkillID not in subskill_id_map:
                missing_ids.append(f"subSkillID {subSkillID}")
            if allContentID not in allcontent_id_map:
                missing_ids.append(f"allContentID {allContentID}")
            print(f"{BColors.FAIL}Skipping skill section {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Skill sections migration completed{BColors.ENDC}")
    return skillsection_id_map
