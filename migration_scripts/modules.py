from datetime import datetime
import pytz
from BColors import BColors

def migrate_modules(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating modules...{BColors.ENDC}")
    module_id_map = {}
    org_id_map = kwargs["org_id_map"]
    icon_id_map = kwargs["icon_id_map"]
    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        status = document.get("status")
        priorityIndex = document.get("priorityIndex")
        iconID = str(document.get("iconID"))
        organizationId = str(document.get("OrganizationId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        # Map MongoDB organization and icon IDs to PostgreSQL IDs
        postgres_organization_id = org_id_map.get(str(organizationId))
        postgres_icon_id = icon_id_map.get(str(iconID))

        if organizationId in org_id_map and iconID in icon_id_map:
            # Insert the module record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Module" ("name", "status", "priorityIndex", "iconId", "organizationId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, status, priorityIndex, postgres_icon_id, postgres_organization_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            module_id_map[str(mongo_id)] = new_id
        else:
            print(f"{BColors.FAIL}Skipping module {mongo_id} because it isn't associated to either an organization or an icon{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Modules migration completed{BColors.ENDC}")
    return module_id_map
