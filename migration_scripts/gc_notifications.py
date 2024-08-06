from datetime import datetime
import pytz
from BColors import BColors

def migrate_gc_notifications(cursor, postgres_cursor, **kwargs):
    """Migrate gc_notifications collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating GCNotifications...{BColors.ENDC}")
    gc_experience_id_map = kwargs["gc_experience_id_map"]
    gc_notification_id_map = {}

    for document in cursor:
        
        mongo_id = document.get("_id")
        title = document.get("title")
        description = document.get("description")
        type = document.get("type")
        is_announcement = document.get("isAnnouncement")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        experienceId = str(document.get("experience"))
        
        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        # Edge case for gc_experience having no organization: Any gc_experience with no organization is ignored.
        if experienceId in gc_experience_id_map.keys():
            gc_exp_id_to_assign = gc_experience_id_map[str(experienceId)]
            query = 'INSERT INTO public."GCNotification" ("experienceId", "title", "description", "type", "isAnnouncement", "createdAt", "updatedAt" ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (gc_exp_id_to_assign, title, description, type, is_announcement, createdAt, updatedAt)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            gc_notification_id_map[str(mongo_id)] = new_id
        else:
            print(f"{BColors.FAIL}Skipping gc_notification {mongo_id} due to invalid experienceId: {experienceId}{BColors.ENDC}")

        

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_notification_id_map
