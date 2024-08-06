from datetime import datetime
import pytz
from BColors import BColors

def migrate_skills(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating skills...{BColors.ENDC}")
    skill_id_map = {}
    lesson_id_map = kwargs["lessons_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        name = document.get("name")
        status = document.get("status")
        priorityIndex = document.get("priorityIndex")
        lessonID = str(document.get("lessonID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the lessonID exists in the corresponding map
        if lessonID in lesson_id_map:
            postgres_lesson_id = lesson_id_map[lessonID]

            # Insert the skill record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Skill" ("name", "status", "priorityIndex", "lessonId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (name, status, priorityIndex, postgres_lesson_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            skill_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping skill {mongo_id} due to missing lessonID {lessonID}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Skills migration completed{BColors.ENDC}")
    return skill_id_map
