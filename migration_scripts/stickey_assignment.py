from datetime import datetime
import pytz
from BColors import BColors

def migrate_stickeyassignments(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating stickey assignments...{BColors.ENDC}")
    stickey_assignment_id_map = {}
    org_id_map = kwargs["org_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        title = document.get("title")
        description = document.get("description")
        content = document.get("content")
        points = document.get("points")
        latitude = document.get("latitude")
        longitude = document.get("longitude")
        contentType = document.get("contentType")
        organizationId = str(document.get("OrganizationId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the organizationId exists in the corresponding map
        if organizationId in org_id_map:
            postgres_organization_id = org_id_map[organizationId]

            # Insert the stickey assignment record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."StickyAssignment" ("title", "description", "content", "points", "latitude", "longitude", "contentType", "organizationId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (title, description, content, points, latitude, longitude, contentType, postgres_organization_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            stickey_assignment_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping stickey assignment {mongo_id} due to missing organizationId {organizationId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Stickey assignments migration completed{BColors.ENDC}")
    return stickey_assignment_id_map
