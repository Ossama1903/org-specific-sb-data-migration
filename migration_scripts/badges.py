from datetime import datetime
import pytz
from BColors import BColors

def migrate_badges(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating badges...{BColors.ENDC}")
    badge_id_map = {}
    org_id_map = kwargs["org_id_map"]
    icon_id_map = kwargs["icon_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        description = document.get("description")
        iconID = str(document.get("iconID"))
        organizationId = str(document.get("OrganizationId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the organizationId and iconID exist in the corresponding maps
        if organizationId in org_id_map and iconID in icon_id_map:
            postgres_organization_id = org_id_map[organizationId]
            postgres_icon_id = icon_id_map[iconID]

            # Insert the badge record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Badge" ("name", "description", "iconId", "organizationId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, description, postgres_icon_id, postgres_organization_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            badge_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if organizationId not in org_id_map:
                missing_ids.append(f"organizationId {organizationId}")
            if iconID not in icon_id_map:
                missing_ids.append(f"iconID {iconID}")
            print(f"{BColors.FAIL}Skipping badge {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Badges migration completed{BColors.ENDC}")
    return badge_id_map
