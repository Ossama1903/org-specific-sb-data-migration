from BColors import BColors
from datetime import datetime
import pytz

def migrate_journal_shared_with(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating JournalSharedWith...{BColors.ENDC}")
    journal_id_map = kwargs["journal_id_map"]
    user_id_map = kwargs["user_id_map"]


    for document in cursor:
        journal_id = str(document.get("_id"))
        user_ids_shared_with = document.get("sharedWith")

        if user_ids_shared_with:
            for user in user_ids_shared_with:
                user_id = str(user)
                if user_id in user_id_map and journal_id in journal_id_map:
            
                    insert_query = '''
                    INSERT INTO public."JournalSharedWith" ("userId", "journalId")
                    VALUES (%s, %s) RETURNING id
                    '''    

                    postgres_user_id = user_id_map[user_id]
                    postgres_journal_id = journal_id_map[journal_id]

                    data = (postgres_user_id, postgres_journal_id)
                    postgres_cursor.execute(insert_query, data)
                else:
                    if user_id not in user_id_map:
                        print(f"{BColors.FAIL}Skipping SharedWith entry because user {user_id} is missing{BColors.ENDC}")
                    elif journal_id not in journal_id:
                        print(f"{BColors.FAIL}Skipping SharedWith entry because journal {journal_id} is missing{BColors.ENDC}")

    print(f"{BColors.OKGREEN}JournalSharedWith migration completed{BColors.ENDC}")
    