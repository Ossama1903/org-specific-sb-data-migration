from BColors import BColors
from datetime import datetime
import pytz

def migrate_formquestions(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating form questions...{BColors.ENDC}")
    form_question_id_map = {}
    form_id_map = kwargs["form_id_map"]

    for document in cursor:
        form_id = str(document.get("_id"))
        form_questions = document.get("questions")
        
        if form_id not in form_id_map:
            print(f"{BColors.FAIL}Skipping form questions for form_id {form_id} because it doesn't exist in form_id_map{BColors.ENDC}")
            continue
        
        for question in form_questions:
            if question:
                mongo_id = str(question.get("_id"))
                open = question.get("open")
                questionImage = question.get("questionImage")
                trueValue = question.get("trueValue", 0)
                questionText = question.get("questionText")
                postgres_form_id = form_id_map[form_id]

                current_time = str(datetime.now(pytz.UTC)).split("+")[0]
                createdAt = current_time
                updatedAt = current_time

                insert_query = '''
                INSERT INTO public."FormQuestion" ("open", "questionText", "questionImage", "trueValue", "formId", "createdAt", "updatedAt")
                VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id
                '''         

                data = (open, questionText, questionImage, trueValue, postgres_form_id, createdAt, updatedAt)
                postgres_cursor.execute(insert_query, data)
                new_id = postgres_cursor.fetchone()[0]
                form_question_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}FormQuestions migration completed ✓{BColors.ENDC}")
    return form_question_id_map
