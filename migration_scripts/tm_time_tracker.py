from datetime import datetime
import pytz
from BColors import BColors

def migrate_tmtimetracker(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating TMTimeTracker...{BColors.ENDC}")
    tmtimetracker_id_map = {}
    user_id_map = kwargs["user_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        projectName = document.get("projectName")
        jobName = document.get("jobName")
        trackingDate = document.get("trackingDate")
        punchIn = document.get("punchIn")
        punchOut = document.get("punchOut")
        note = document.get("note")
        label = document.get("label")
        user = str(document.get("user"))

        print(user)
        # Check if the user exists in the corresponding map
        if user in user_id_map:
            postgres_user_id = user_id_map[user]


            # Insert the TMTimeTracker record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."TMTimeTracker" ("projectName", "jobName", "trackingDate", "punchIn", "punchOut", "note", "label", "user_id")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (projectName, jobName, trackingDate, punchIn, punchOut, note, label, postgres_user_id)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            tmtimetracker_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping TMTimeTracker {mongo_id} due to missing user {user}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}TMTimeTracker migration completed{BColors.ENDC}")
    return tmtimetracker_id_map
