from datetime import datetime
import pytz
from BColors import BColors

def migrate_permissions(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating permissions...{BColors.ENDC}")
    permission_id_map = {}
    admin_id_map = kwargs["admin_id_map"]

    for document in cursor:
        mongo_id = document.get("_id")
        table_name = document.get("tableName")
        mode = document.get("mode")
        admin_id = str(document.get("adminID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        
        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = createdAt or current_time
            updatedAt = updatedAt or current_time

        if admin_id in admin_id_map:
            admin_id_to_assign = admin_id_map[admin_id]
            # Insert the permission record into the database
            insert_query = 'INSERT INTO public."Permission" ("tableName", "mode", "adminId", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s, %s) RETURNING id'
            data = (table_name, mode, admin_id_to_assign, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            permission_id_map[str(mongo_id)] = new_id

    print(f"{BColors.OKGREEN}Permissions migration completed ✓{BColors.ENDC}")
    return permission_id_map