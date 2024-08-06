from datetime import datetime
import pytz
from BColors import BColors

def migrate_journals(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating journals...{BColors.ENDC}")
    journal_id_map = {}
    user_id_map = kwargs["user_id_map"]
    teacher_id_map = kwargs["teacher_id_map"]
    

    for document in cursor:
        mongo_id = str(document.get("_id"))
        title = document.get("title")
        question = document.get("question")
        answer = document.get("answer")
        teacher = str(document.get("teacher"))
        isAnswered = document.get("isAnswered")
        journal_type = document.get("type")
        content = document.get("content")
        userId = str(document.get("userId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        attachment = document.get("attachment")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the userId exists in the corresponding map
        if userId in user_id_map:
            postgres_user_id = user_id_map[userId]


            # Insert the journal record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Journal" ("title", "question", "answer", "teacher", "isAnswered", "type", "content", "userId", "createdAt", "updatedAt", "attachment")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (title, question, answer, teacher, isAnswered, journal_type, content, postgres_user_id, createdAt, updatedAt, attachment)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            journal_id_map[mongo_id] = new_id
        else:
            if userId not in user_id_map:
                print(f"{BColors.FAIL}Skipping journal {mongo_id} due to missing userId {userId}{BColors.ENDC}")


    print(f"{BColors.OKGREEN}Journals migration completed{BColors.ENDC}")
    return journal_id_map
