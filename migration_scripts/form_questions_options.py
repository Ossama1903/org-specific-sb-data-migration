from BColors import BColors
from datetime import datetime
import pytz

def migrate_form_questions_options(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating form questions options...{BColors.ENDC}")
    form_question_options_id_map = {}
    form_id_map = kwargs["form_id_map"]
    form_question_id_map = kwargs["form_question_id_map"]

    for document in cursor:
        form_id = str(document.get("_id"))
        form_questions = document.get("questions")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        
        if form_id not in form_id_map:
            print(f"{BColors.FAIL}Skipping form question options for form_id {form_id} because it doesn't exist in form_id_map{BColors.ENDC}")
            continue

        for question in form_questions:
            options = question.get("options")
            form_question_id = str(question.get("_id"))

            if form_question_id not in form_question_id_map:
                print(f"{BColors.FAIL}Skipping form question options for form_question_id {form_question_id} because it doesn't exist in form_question_id_map{BColors.ENDC}")
                continue

            postgres_form_id = form_question_id_map[form_question_id]
            for option in options:
                value = option.get("optionValue", 0)
                image = option.get("optionImage")
                mongo_id = str(option.get("_id"))
                text = option.get("optionText")

                insert_query = '''
                INSERT INTO public."FormQuestionOption" ("optionText", "optionImage", "optionValue", "formQuestionId", "createdAt", "updatedAt")
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
                '''     
                data = (text, image, value, postgres_form_id, createdAt, updatedAt)
                postgres_cursor.execute(insert_query, data)
                new_id = postgres_cursor.fetchone()[0]
                form_question_options_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}FormQuestionsOptions migration completed ✓{BColors.ENDC}")
    return form_question_options_id_map
