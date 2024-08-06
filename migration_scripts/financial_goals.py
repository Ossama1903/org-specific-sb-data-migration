from datetime import datetime
import pytz
from BColors import BColors

def migrate_financialgoals(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating financial goals...{BColors.ENDC}")
    financialgoal_id_map = {}
    user_id_map = kwargs["user_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        status = document.get("status")
        created_id = document.get("created_id")
        completed_id = document.get("completed_id")
        isDeleted = document.get("isDeleted")
        start_date = document.get("start_date")
        description = document.get("description")
        name = document.get("name")
        userId = str(document.get("userId"))
        goal_type = document.get("type")
        end_date = document.get("end_date")
        email = document.get("email", "")
        frequency = document.get("frequency", 0)
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the userId exists in the corresponding map
        if userId in user_id_map:
            postgres_user_id = user_id_map[userId]

            # Insert the financial goal record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."FinancialGoal" ("status", "createdId", "completedId", "isDeleted", "startDate", "description", "name", "userId", "type", "endDate", "createdAt", "updatedAt", "email", "frequency")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (status, created_id, completed_id, isDeleted, start_date, description, name, postgres_user_id, goal_type, end_date, createdAt, updatedAt, email, frequency)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            financialgoal_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping financial goal {mongo_id} due to missing userId {userId}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Financial goals migration completed{BColors.ENDC}")
    return financialgoal_id_map
