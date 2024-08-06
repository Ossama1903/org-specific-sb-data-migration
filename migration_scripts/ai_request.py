from datetime import datetime
import pytz
from BColors import BColors

def migrate_ai_requests(cursor, postgres_cursor, **kwargs):
    print("FROM AIRequest")
    print(f"{BColors.WARNING}Migrating AI requests...{BColors.ENDC}")
    ai_request_id_map = {}
    admin_id_map = kwargs["admin_id_map"]
    for document in cursor:
        mongo_id = str(document.get("_id"))
        adminId = str(document.get("adminId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = createdAt or current_time
            updatedAt = updatedAt or current_time

        # Check if the adminId already exists in the database
        check_query = 'SELECT EXISTS(SELECT 1 FROM public."AIRequest" WHERE "adminId" = %s)'
        postgres_cursor.execute(check_query, (admin_id_map.get(adminId),))
        if postgres_cursor.fetchone()[0]:
            print(f"{BColors.FAIL}Skipping ai-request {mongo_id} because duplicate adminId: {adminId}{BColors.ENDC}")
            continue

        if adminId in admin_id_map:
            postgres_admin_id = admin_id_map[adminId]
            # Insert the AIRequest record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."AIRequest" ("adminId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s) RETURNING id
            '''
            data = (postgres_admin_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            ai_request_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping ai-request {mongo_id} because it isn't associated to an admin{BColors.ENDC}")

    print(f"{BColors.OKGREEN}AI requests migration completed{BColors.ENDC}")
    return ai_request_id_map
