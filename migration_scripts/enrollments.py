from datetime import datetime
import pytz
from BColors import BColors

def migrate_enrollments(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating enrollments...{BColors.ENDC}")
    enrollment_id_map = {}
    subskill_id_map = kwargs.get("subskill_id_map", {})
    user_id_map = kwargs["user_id_map"]
    word_id_map = kwargs.get("word_id_map", {})
    lesson_id_map = kwargs.get("lesson_id_map", {})
    module_id_map = kwargs.get("module_id_map", {})
    skill_id_map = kwargs.get("skill_id_map", {})

    for document in cursor:
        mongo_id = str(document.get("_id"))
        quizPoints = document.get("quizPoints")
        wordID = str(document.get("wordID")) if document.get("wordID") else None
        lessonID = str(document.get("lessonID")) if document.get("lessonID") else None
        moduleID = str(document.get("moduleID")) if document.get("moduleID") else None
        skillID = str(document.get("skillID")) if document.get("skillID") else None
        subSkillID = str(document.get("subSkillID")) if document.get("subSkillID") else None
        userID = str(document.get("userID"))
        rating = document.get("rating")
        isCompleted = document.get("isCompleted")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Validate and map the non-null ID
        valid_id = None
        id_type = None

        if wordID and wordID in word_id_map:
            valid_id = word_id_map[wordID]
            id_type = "wordId"
        elif lessonID and lessonID in lesson_id_map:
            valid_id = lesson_id_map[lessonID]
            id_type = "lessonId"
        elif moduleID and moduleID in module_id_map:
            valid_id = module_id_map[moduleID]
            id_type = "moduleId"
        elif skillID and skillID in skill_id_map:
            valid_id = skill_id_map[skillID]
            id_type = "skillId"
        elif subSkillID and subSkillID in subskill_id_map:
            valid_id = subskill_id_map[subSkillID]
            id_type = "subSkillId"
        else:
            print(f"{BColors.FAIL}Skipping enrollment {mongo_id} due to missing valid ID{BColors.ENDC}")
            continue

        if userID in user_id_map:
            postgres_user_id = user_id_map[userID]

            # Check if a similar enrollment entry already exists to avoid duplicate records
            check_query = f'SELECT EXISTS(SELECT 1 FROM public."Enrollment" WHERE "userId" = %s AND "{id_type}" = %s)'
            postgres_cursor.execute(check_query, (postgres_user_id, valid_id))
            if postgres_cursor.fetchone()[0]:
                print(f"Skipping existing enrollment for user: {userID} and {id_type}: {valid_id}")
                continue

            # Insert the enrollment record into the PostgreSQL database
            insert_query = f'''
            INSERT INTO public."Enrollment" ("quizPoints", "{id_type}", "userId", "rating", "isCompleted", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (quizPoints, valid_id, postgres_user_id, rating, isCompleted, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            enrollment_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping enrollment {mongo_id} due to missing userID {userID}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Enrollments migration completed{BColors.ENDC}")
    return enrollment_id_map
