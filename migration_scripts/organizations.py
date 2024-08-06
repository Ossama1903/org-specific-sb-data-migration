from BColors import BColors

def migrate_organizations(cursor, postgres_cursor, org_names):
    """Migrate specified organizations collection to PostgreSQL."""
    print(f"{BColors.WARNING}Migrating specified organizations...{BColors.ENDC}")
    org_id_map = {}
    
    for document in cursor:
        name = document.get("name")
        if name not in org_names:
            continue

        mongo_id = document.get("_id")
        wait_time = document.get("wait_time", 30)
        created_at = document.get("createdAt")
        updated_at = document.get("updatedAt")
        query = 'INSERT INTO public."Organization" ("name", "waitTime", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s) RETURNING id'
        data = (name, wait_time, created_at, updated_at)
        postgres_cursor.execute(query, data)
        new_id = postgres_cursor.fetchone()[0]
        org_id_map[str(mongo_id)] = new_id

    print(f"{BColors.OKGREEN}Migration of specified organizations completed ✓{BColors.ENDC}")
    return org_id_map
