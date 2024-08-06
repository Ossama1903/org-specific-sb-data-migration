from datetime import datetime
import pytz
from BColors import BColors

def migrate_gc_participant_members(cursor, postgres_cursor, **kwargs):
    """Migrate gc_participant_members collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating GCParticipantMembers...{BColors.ENDC}")
    
    gc_participant_id_map = kwargs["gc_participant_id_map"]
    user_id_map = kwargs["user_id_map"]

    gc_mission_text_answer_id_map = {}

    for document in cursor:
        
        participant_id = str(document.get("_id"))
        members = document.get("members")


        for member in members:
            user_id = str(member)
            if user_id in user_id_map.keys():
                postgres_participant_id = gc_participant_id_map[participant_id]
                postgres_user_id = user_id_map[user_id]
                query = 'INSERT INTO public."GCParticipantMember" ("gcParticipantId", "userId") VALUES (%s, %s) RETURNING id'
                data = (postgres_participant_id, postgres_user_id)
                postgres_cursor.execute(query, data)
            else:
                if user_id not in user_id_map.keys():
                    print(f"{BColors.FAIL}Skipping participant_member due to invalid userId: {user_id}{BColors.ENDC}")
                else:
                    print(f"{BColors.FAIL}Skipping participant_member due to invalid participantId: {participant_id}{BColors.ENDC}")
                   

        

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_mission_text_answer_id_map
