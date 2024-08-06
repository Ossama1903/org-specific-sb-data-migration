from datetime import datetime
import pytz
from BColors import BColors

def migrate_forms(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating forms...{BColors.ENDC}")
    form_id_map = {}
    org_id_map = kwargs["org_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        description = document.get("description")
        stared = document.get("stared")
        formType = document.get("formType")
        name = document.get("name")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        organizationId = str(document.get("OrganizationId"))
        success_description = document.get("success_description", "")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        if organizationId in org_id_map:
            postgres_org_id = org_id_map[organizationId]

            # Insert the form record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Form" ("description", "stared", "formType", "name", "createdAt", "updatedAt", "organization_id", "successDescription")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (description, stared, formType, name, createdAt, updatedAt, postgres_org_id, success_description)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            form_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping form {mongo_id} due to missing organizationId {organizationId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Forms migration completed{BColors.ENDC}")
    return form_id_map
