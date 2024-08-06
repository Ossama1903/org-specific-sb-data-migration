from datetime import datetime
import pytz
from BColors import BColors

def migrate_moneysubskills(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating money subskills...{BColors.ENDC}")
    moneysubskill_id_map = {}
    moneyskill_id_map = kwargs["moneyskill_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        description = document.get("description")
        moneySkillId = str(document.get("moneySkillId"))
        image = document.get("image")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the moneySkillId exists in the corresponding map
        if moneySkillId in moneyskill_id_map:
            postgres_moneyskill_id = moneyskill_id_map[moneySkillId]

            # Insert the money subskill record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."MoneySubSkill" ("name", "description", "moneySkillId", "image", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, description, postgres_moneyskill_id, image, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            moneysubskill_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping money subskill {mongo_id} due to missing moneySkillId {moneySkillId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Money subskills migration completed{BColors.ENDC}")
    return moneysubskill_id_map
