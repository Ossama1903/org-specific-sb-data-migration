from datetime import datetime
import pytz
from BColors import BColors

def migrate_podcasts(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating podcasts...{BColors.ENDC}")
    podcast_id_map = {}
    org_id_map = kwargs["org_id_map"]
    for document in cursor:
        mongo_id = document.get("_id")
        assigned = document.get("assigned")
        title = document.get("title")
        description = document.get("description")
        totalPoints = document.get("totalPoints")
        organizationId = document.get("organization")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        
        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        if str(organizationId) in org_id_map:
            org_id_to_assign = org_id_map[str(organizationId)]
            insert_query = 'INSERT INTO public."Podcast" ("assigned", "title", "description", "totalPoints", "organizationId", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (assigned, title, description, totalPoints, org_id_to_assign, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            podcast_id_map[str(mongo_id)] = new_id
        else: 
            print(f"{BColors.FAIL}Skipping podcast {mongo_id} because it isn't associated to an organization{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Podcasts migration completed{BColors.ENDC}")
    return podcast_id_map
