from datetime import datetime
import pytz
from BColors import BColors

def migrate_gc_missions(cursor, postgres_cursor, **kwargs):
    """Migrate gc_missions[ts] collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating GCMissions...{BColors.ENDC}")
    gc_experience_id_map = kwargs["gc_experience_id_map"]
    gc_mission_id_map = {}

    for document in cursor:
        
        mongo_id = document.get("_id")
        name = document.get("name")
        description = document.get("description")
        image_url = document.get("imageUrl")
        additional_info_link = document.get("additionalInfoLink")
        show_on_feed = document.get("shownOnFeed")
        status = document.get("status")
        type = document.get("type")
        points = document.get("points")
        media_type = document.get("mediaType")
        media_source = document.get("mediaSource")
        location_lat = document.get("locationLat")
        location_lng = document.get("locationLng")
        acceptable_meter_distance = document.get("acceptableMeterDistance")
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
            query = 'INSERT INTO public."GCMission" ("name", "description", "imageUrl", "additionalInfoLink", "shownOnFeed", "status", "type", "points", "mediaType", "mediaSource", "locationLat", "locationLng", "acceptableMeterDistance", "createdAt", "updatedAt", "gcExperienceId" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (name, description, image_url, additional_info_link, show_on_feed, status, type, points, media_type, media_source, location_lat, location_lng, acceptable_meter_distance, createdAt, updatedAt, gc_exp_id_to_assign)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            gc_mission_id_map[str(mongo_id)] = new_id
        else:
            print(f"{BColors.FAIL}Skipping gc_mission {mongo_id} due to invalid experienceId: {experienceId}{BColors.ENDC}")

        

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_mission_id_map
