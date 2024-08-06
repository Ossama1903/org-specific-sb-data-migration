from datetime import datetime
import pytz
from BColors import BColors

def migrate_gc_participants(cursor, postgres_cursor, **kwargs):
    """Migrate gc_participants collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating GCParticipants...{BColors.ENDC}")
    
    gc_experience_id_map = kwargs["gc_experience_id_map"]
    user_id_map = kwargs["user_id_map"]
    
    gc_participants_id_map = {}

    for document in cursor:
        
        mongo_id = document.get("_id")
        name = document.get("name")
        createdById = str(document.get("createdBy"))
        experienceId = str(document.get("experience"))
        image_url = document.get("imageUrl")
        passcode = document.get("passCode")

        # Edge case for gc_experience having no organization: Any gc_experience with no organization is ignored.
        if experienceId in gc_experience_id_map.keys():
            gc_exp_id_to_assign = gc_experience_id_map[str(experienceId)]
            user_id_to_assign = None 
            if createdById in user_id_map:
                user_id_to_assign = user_id_map[str(createdById)]
            query = 'INSERT INTO public."GCParticipant" ("name", "imageUrl", "passcode", "createdByUserId", "gcExperienceId") VALUES (%s, %s, %s, %s, %s) RETURNING id'
            data = (name, image_url, passcode, user_id_to_assign, gc_exp_id_to_assign)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            gc_participants_id_map[str(mongo_id)] = new_id
        else:
            print(f"{BColors.FAIL}Skipping gc_participant {mongo_id} due to invalid experienceId: {experienceId}{BColors.ENDC}")

        

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_participants_id_map
