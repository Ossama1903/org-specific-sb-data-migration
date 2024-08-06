from datetime import datetime
import pytz
from BColors import BColors

def migrate_stickeyassignmentsusers(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating stickey assignments users...{BColors.ENDC}")
    stickey_assignment_user_id_map = {}
    user_id_map = kwargs["user_id_map"]
    stickey_assignment_id_map = kwargs["stickey_assignment_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        status = document.get("status")
        approval = document.get("approval")
        userId = str(document.get("userId"))
        stickeyAssignmentId = str(document.get("stickeyAssignmentId"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the userId and stickeyAssignmentId exist in the corresponding maps
        if userId in user_id_map and stickeyAssignmentId in stickey_assignment_id_map:
            postgres_user_id = user_id_map[userId]
            postgres_stickey_assignment_id = stickey_assignment_id_map[stickeyAssignmentId]


            # Insert the stickey assignment user record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."StickyAssignmentUser" ("status", "approval", "user_id", "sticky_assignment_id", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (status, approval, postgres_user_id, postgres_stickey_assignment_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            stickey_assignment_user_id_map[mongo_id] = new_id
        else:
            missing_ids = []
            if userId not in user_id_map:
                missing_ids.append(f"userId {userId}")
            if stickeyAssignmentId not in stickey_assignment_id_map:
                missing_ids.append(f"stickeyAssignmentId {stickeyAssignmentId}")
            print(f"{BColors.FAIL}Skipping stickey assignment user {mongo_id} due to missing {', '.join(missing_ids)}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Stickey assignments users migration completed{BColors.ENDC}")
    return stickey_assignment_user_id_map
