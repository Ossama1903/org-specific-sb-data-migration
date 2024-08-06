from BColors import BColors
from datetime import datetime
import pytz

def migrate_form_sections(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating form sections...{BColors.ENDC}")
    form_section_id_map = {}
    form_id_map = kwargs["form_id_map"]

    for document in cursor:
        form_id = str(document.get("_id"))
        form_sections = document.get("section")

        if form_id not in form_id_map:
            print(f"{BColors.FAIL}Skipping form sections for form_id {form_id} because it doesn't exist in form_id_map{BColors.ENDC}")
            continue

        if form_sections:
            for section in form_sections:
                if section:
                    mongo_id = str(section.get("_id"))
                    name = section.get("sectionName")
                    postgres_form_id = form_id_map[form_id]

                    insert_query = '''
                    INSERT INTO public."FormSection" ("sectionName", "formId")
                    VALUES (%s, %s) RETURNING id
                    '''         

                    data = (name, postgres_form_id)
                    postgres_cursor.execute(insert_query, data)
                    new_id = postgres_cursor.fetchone()[0]
                    form_section_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}FormSections migration completed ✓{BColors.ENDC}")
    return form_section_id_map
