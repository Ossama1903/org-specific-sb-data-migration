from datetime import datetime
import pytz
from BColors import BColors

def migrate_gc_submissions(cursor, postgres_cursor, **kwargs):
    """Migrate gc_submissions collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating GCSubmissions...{BColors.ENDC}")
    gc_mission_id_map = kwargs["gc_mission_id_map"]
    gc_participant_id_map = kwargs["gc_participant_id_map"]

    gc_submission_id_map = {}

    for document in cursor:
        
        mongo_id = document.get("_id")
        type = document.get("type")
        text_answer = document.get("textAnswer")
        media_caption = document.get("mediaCaption")
        media_url = document.get("mediaUrl")
        location_caption = document.get("locationCaption")
        location_lat = document.get("locationLat")
        location_lng = document.get("locationLng")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        mission_id = str(document.get("mission"))
        participant_id = str(document.get("participant"))
        
        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        # Edge case for gc_experience having no organization: Any gc_experience with no organization is ignored.
        if mission_id in gc_mission_id_map.keys() and participant_id in gc_participant_id_map:
            gc_mission_id_to_assign = gc_mission_id_map[str(mission_id)]
            gc_participant_id_to_assign = gc_participant_id_map[str(participant_id)]
            query = 'INSERT INTO public."GCSubmission" ("type", "textAnswer", "mediaCaption", "mediaUrl", "locationCaption", "locationLat", "locationLng", "missionId", "createdAt", "updatedAt", "participantId" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (type, text_answer, media_caption, media_url, location_caption, location_lat, location_lng, gc_mission_id_to_assign, createdAt, updatedAt, gc_participant_id_to_assign)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            gc_mission_id_map[str(mongo_id)] = new_id
        else:
            if mission_id in gc_mission_id_map.keys():
                print(f"{BColors.FAIL}Skipping gc_submission {mongo_id} due to invalid missionId: {mission_id}{BColors.ENDC}")
            else: 
                print(f"{BColors.FAIL}Skipping gc_submission {mongo_id} due to invalid participantId: {participant_id}{BColors.ENDC}")

        

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_mission_id_map
