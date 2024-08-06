from datetime import datetime
import pytz
from BColors import BColors

def migrate_quizzes(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating quizzes...{BColors.ENDC}")
    quiz_id_map = {}
    subskill_id_map = kwargs["subskill_id_map"]
    icon_id_map = kwargs["icon_id_map"]
    org_id_map = kwargs["org_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        question = document.get("question")
        answer01 = document.get("answer01")
        answer02 = document.get("answer02")
        answer03 = document.get("answer03")
        answer04 = document.get("answer04")
        trueOption = document.get("trueOption")
        points = document.get("points")
        iconID = str(document.get("iconID"))
        subSkillID = str(document.get("subSkillID"))
        organizationId = str(document.get("OrganizationId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Validate and map IDs
        if subSkillID in subskill_id_map:
            postgres_subskill_id = subskill_id_map[subSkillID]
            postgres_org_id = org_id_map[organizationId]

            postgres_icon_id = None
            if iconID in icon_id_map:
                postgres_icon_id = icon_id_map[iconID]

            # Insert the quiz record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Quiz" ("question", "answer01", "answer02", "answer03", "answer04", "trueOption", "points", "iconId", "subSkillId", "organizationId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (question, answer01, answer02, answer03, answer04, trueOption, points, postgres_icon_id, postgres_subskill_id, postgres_org_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            quiz_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if subSkillID not in subskill_id_map:
                missing_ids.append(f"subSkillID {subSkillID}")
            if iconID not in icon_id_map:
                missing_ids.append(f"iconID {iconID}")
            if organizationId not in org_id_map:
                missing_ids.append(f"organizationId {organizationId}")
            print(f"{BColors.FAIL}Skipping quiz {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Quizzes migration completed{BColors.ENDC}")
    return quiz_id_map
