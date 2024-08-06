from datetime import datetime
import pytz
from BColors import BColors

def migrate_lesson_badges(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating lesson badges...{BColors.ENDC}")
    lesson_badge_id_map = {}
    lesson_id_map = kwargs["lessons_id_map"]
    badge_id_map = kwargs["badges_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        lessonID = str(document.get("lessonID"))
        badgeID = str(document.get("badgeID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the lessonID and badgeID exist in the corresponding maps
        if lessonID in lesson_id_map and badgeID in badge_id_map:
            postgres_lesson_id = lesson_id_map[lessonID]
            postgres_badge_id = badge_id_map[badgeID]

            # Insert the lesson badge record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."LessonBadge" ("lessonId", "badgeId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s) RETURNING id
            '''
            data = (postgres_lesson_id, postgres_badge_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            lesson_badge_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if lessonID not in lesson_id_map:
                missing_ids.append(f"lessonID {lessonID}")
            if badgeID not in badge_id_map:
                missing_ids.append(f"badgeID {badgeID}")
            print(f"{BColors.FAIL}Skipping lesson badge {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Lesson badges migration completed{BColors.ENDC}")
    return lesson_badge_id_map
