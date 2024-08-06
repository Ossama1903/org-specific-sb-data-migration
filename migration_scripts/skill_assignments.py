from datetime import datetime
import pytz
from BColors import BColors

def migrate_skillassignments(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating skill assignments...{BColors.ENDC}")
    skillassignment_id_map = {}
    org_id_map = kwargs["org_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        applicationName = document.get("applicationName")
        partName = document.get("partName")
        assignmentName = document.get("assignmentName")
        iframeLink = document.get("iframeLink")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        organizationId = str(document.get("OrganizationId"))

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the organizationId exists in the corresponding map
        if organizationId in org_id_map:
            postgres_organization_id = org_id_map[organizationId]

            # Insert the skill assignment record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."SkillAssignment" ("applicationName", "partName", "assignmentName", "iframeLink", "organizationId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (applicationName, partName, assignmentName, iframeLink, postgres_organization_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            skillassignment_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping skill assignment {mongo_id} due to missing organizationId {organizationId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Skill assignments migration completed{BColors.ENDC}")
    return skillassignment_id_map
