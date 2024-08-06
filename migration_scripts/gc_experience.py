from datetime import datetime
import pytz
from BColors import BColors

def migrate_gc_experience(cursor, postgres_cursor, **kwargs):
    """Migrate gc_experiences collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating gcExperience...{BColors.ENDC}")
    org_id_map = kwargs["org_id_map"]
    gc_experience_id_map = {}
    for document in cursor:
        mongo_id = document.get("_id")
        name = document.get("name")
        description = document.get("description")
        branding_photo_url = document.get("brandingPhotoUrl")
        location = document.get("location")
        password = document.get("password")
        image_url = document.get("imageUrl")
        branding_tos = document.get("brandingTos")
        status = document.get("status")
        duration_type = document.get("durationType")
        start_time = document.get("startTime")
        end_time = document.get("endTime")
        duration = document.get("duration")
        participant_type = document.get("participantType")
        participant_allowed_to_create = document.get("participantAllowedToCreate")
        join_code = document.get("joinCode")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        organizationId = str(document.get("organization"))
        
        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = createdAt or current_time
            updatedAt = updatedAt or current_time

        # Edge case for gc_experience having no organization: Any gc_experience with no organization is ignored.
        if organizationId in org_id_map:
            org_id_to_assign = org_id_map[str(organizationId)]
            query = 'INSERT INTO public."GCExperience" ("organizationId", "name", "description", "location", "password", "imageUrl", "brandingPhotoUrl", "brandingTos", "status", "durationType", "startTime", "endTime", "duration", "participantType", "participantAllowedToCreate", "joinCode", "createdAt", "updatedAt" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (org_id_to_assign, name, description, location, password, image_url, branding_photo_url, branding_tos, status, duration_type, start_time, end_time, duration, participant_type, participant_allowed_to_create, join_code, createdAt, updatedAt)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            gc_experience_id_map[str(mongo_id)] = new_id
        else:
            print(f"{BColors.FAIL}Skipping gc_experience {mongo_id} due to invalid organizationId: {organizationId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_experience_id_map