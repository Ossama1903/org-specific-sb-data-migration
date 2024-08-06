from datetime import datetime
import pytz
from BColors import BColors

def migrate_moneyskillsections(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating money skill sections...{BColors.ENDC}")
    moneyskillsection_id_map = {}
    moneysubskill_id_map = kwargs["moneysubskill_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        content = document.get("content")
        contentType = document.get("contentType")
        moneySubSkillId = str(document.get("moneySubSkillId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the moneySubSkillId exists in the corresponding map
        if moneySubSkillId in moneysubskill_id_map:
            postgres_moneysubskill_id = moneysubskill_id_map[moneySubSkillId]

            # Insert the money skill section record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."MoneySkillSection" ("name", "content", "contentType", "moneySubSkillId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, content, contentType, postgres_moneysubskill_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            moneyskillsection_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping money skill section {mongo_id} due to missing moneySubSkillId {moneySubSkillId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Money skill sections migration completed{BColors.ENDC}")
    return moneyskillsection_id_map
