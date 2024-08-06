from datetime import datetime
import pytz
from BColors import BColors

def migrate_notifications(cursor, postgres_cursor, **kwargs):
    print("FROM notifications")
    print(f"{BColors.WARNING}Migrating notifications...{BColors.ENDC}")
    notification_id_map = {}
    org_id_map = kwargs["org_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        organizationId = str(document.get("organization"))
        message = document.get("message")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        fileType = document.get("fileType", "")
        fileUrl = document.get("fileUrl", "")

        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        
        if str(organizationId) in org_id_map:
            # Map MongoDB organization ID to PostgreSQL organization ID using the provided mapping
            postgres_organization_id = org_id_map.get(str(organizationId))
            
            # Insert the notification record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Notification" ("organizationId", "message", "createdAt", "updatedAt", "fileType", "fileUrl")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (postgres_organization_id, message, createdAt, updatedAt, fileType, fileUrl)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            notification_id_map[str(mongo_id)] = new_id
            print(f"Notification migrated with ID {new_id}")
        else:
            print(f"{BColors.FAIL}Skipping notification {mongo_id} because it isn't associated to an organization{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Notifications migration completed{BColors.ENDC}")
    return notification_id_map
