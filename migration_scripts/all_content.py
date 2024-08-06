from datetime import datetime
import pytz
from BColors import BColors

def migrate_allcontents(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating all contents...{BColors.ENDC}")
    allcontent_id_map = {}
    form_id_map = kwargs["form_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        description = document.get("description")
        content_type = document.get("type")
        points = document.get("points")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        content = document.get("content")
        
        if str(content) in form_id_map and content_type == "GoogleForm":
            content = form_id_map[content]


        # Skip records with points greater than 10000 or less than -10000
        if points is not None:
            try:
                points = int(points)
                if points > 10000 or points < -10000:
                    print(f"{BColors.FAIL}Skipping content {mongo_id} due to points value out of range: {points}{BColors.ENDC}")
                    continue
            except ValueError:
                print(f"{BColors.FAIL}Skipping content {mongo_id} due to invalid points value: {points}{BColors.ENDC}")
                continue

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Insert the content record into the PostgreSQL database
        insert_query = '''
        INSERT INTO public."AllContent" ("name", "description", "content", "type", "points", "createdAt", "updatedAt")
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
        '''
        data = (name, description, content, content_type, points, createdAt, updatedAt)
        postgres_cursor.execute(insert_query, data)
        new_id = postgres_cursor.fetchone()[0]
        allcontent_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}All contents migration completed{BColors.ENDC}")
    return allcontent_id_map
