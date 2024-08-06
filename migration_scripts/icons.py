from BColors import BColors

def migrate_icons(cursor, postgres_cursor, **kwargs):
    """Migrate icons collection to PostgreSQL."""
    print(f"{BColors.WARNING}Migrating icons...{BColors.ENDC}")
    org_id_map = kwargs["org_id_map"]
    icon_id_map = {}
    for document in cursor:
        
        mongo_id = document.get("_id")
        name = document.get("name")
        svg = document.get("svg")
        created_at = document.get("createdAt")
        updated_at = document.get("updatedAt")
        organizationId = str(document.get("OrganizationId"))

        # Only migrate icons if the organizationId is in the org_id_map
        if organizationId in org_id_map:
            org_id_to_assign = org_id_map[organizationId]
            query = 'INSERT INTO public."Icon" ("name", "svg", "organizationId", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s, %s) RETURNING id'
            data = (name, svg, org_id_to_assign, created_at, updated_at)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            icon_id_map[str(mongo_id)] = new_id

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return icon_id_map
