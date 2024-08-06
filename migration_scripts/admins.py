from datetime import datetime
import pytz
from BColors import BColors

def migrate_admins(cursor, postgres_cursor, **kwargs):
    """Migrate admins collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating admins...{BColors.ENDC}")
    org_id_map = kwargs["org_id_map"]
    admin_id_map = {}
    for document in cursor:
        mongo_id = document.get("_id")
        username = document.get("username")
        email = document.get("email")
        password = document.get("password")
        picture = document.get("picture")
        blocked = document.get("blocked")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        organizationId = document.get("OrganizationId")
        
        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = createdAt or current_time
            updatedAt = updatedAt or current_time

        # Check if the email already exists in the database
        check_query = 'SELECT EXISTS(SELECT 1 FROM public."Admin" WHERE email = %s)'
        postgres_cursor.execute(check_query, (email,))
        if postgres_cursor.fetchone()[0]:
            print(f"{BColors.FAIL}Skipping already migrated email: {email}{BColors.ENDC}")
            continue

        # Edge case for admin having no organization: Any admin with no organization is ignored.
        if str(organizationId) in org_id_map:
            org_id_to_assign = org_id_map[str(organizationId)]
            query = 'INSERT INTO public."Admin" ("username", "email", "password", "blocked", "picture", "organizationId", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (username, email, password, blocked, picture, org_id_to_assign, createdAt, updatedAt)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            admin_id_map[str(mongo_id)] = new_id

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return admin_id_map
