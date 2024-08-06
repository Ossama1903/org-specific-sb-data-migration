from datetime import datetime
import pytz
from BColors import BColors

def migrate_lessonwordsglossaries(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating lesson words glossaries...{BColors.ENDC}")
    lesson_word_glossary_id_map = {}
    lesson_id_map = kwargs["lesson_id_map"]
    words_glossary_id_map = kwargs["words_glossary_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        lessonID = str(document.get("lessonID"))
        wordsGlossaryID = str(document.get("wordsGlossaryID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the lessonID and wordsGlossaryID exist in the corresponding maps
        if lessonID in lesson_id_map and wordsGlossaryID in words_glossary_id_map:
            postgres_lesson_id = lesson_id_map[lessonID]
            postgres_words_glossary_id = words_glossary_id_map[wordsGlossaryID]

            # Insert the lesson words glossary record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."LessonWordsGlossary" ("lessonId", "wordsGlossaryId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s) RETURNING id
            '''
            data = (postgres_lesson_id, postgres_words_glossary_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            lesson_word_glossary_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if lessonID not in lesson_id_map:
                missing_ids.append(f"lessonID {lessonID}")
            if wordsGlossaryID not in words_glossary_id_map:
                missing_ids.append(f"wordsGlossaryID {wordsGlossaryID}")
            print(f"{BColors.FAIL}Skipping lesson words glossary entry {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Lesson words glossaries migration completed{BColors.ENDC}")
    return lesson_word_glossary_id_map
