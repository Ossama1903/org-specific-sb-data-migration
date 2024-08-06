from datetime import datetime
import pytz
from BColors import BColors

def migrate_analyticssettings(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating analytics settings...{BColors.ENDC}")
    analyticssetting_id_map = {}
    org_id_map = kwargs["org_id_map"]
    form_id_map = kwargs["form_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        organizationId = str(document.get("organizationId"))
        assessmentFormId = str(document.get("assessmentFormId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Validate and map IDs
        if organizationId in org_id_map and assessmentFormId in form_id_map:
            postgres_org_id = org_id_map[organizationId]
            postgres_form_id = form_id_map[assessmentFormId]


            # Insert the analytics setting record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."AnalyticsSetting" ("organizationId", "assessmentFormId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s) RETURNING id
            '''
            data = (postgres_org_id, postgres_form_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            analyticssetting_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if organizationId not in org_id_map:
                missing_ids.append(f"organizationId {organizationId}")
            if assessmentFormId not in form_id_map:
                missing_ids.append(f"assessmentFormId {assessmentFormId}")
            print(f"{BColors.FAIL}Skipping analytics setting {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Analytics settings migration completed{BColors.ENDC}")
    return analyticssetting_id_map
