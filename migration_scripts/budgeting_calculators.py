from datetime import datetime
import pytz
from BColors import BColors

def migrate_budgetingcalculators(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating budgeting calculators...{BColors.ENDC}")
    budgetingcalculator_id_map = {}
    user_id_map = kwargs["user_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        amount = document.get("amount")
        mainCategory = document.get("mainCategory")
        subCategory = document.get("subCategory")
        calc_type = document.get("type")
        name = document.get("name")
        description = document.get("description")
        frequency = document.get("frequency")
        userID = str(document.get("userID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        if userID in user_id_map:
            postgres_user_id = user_id_map[userID]

            # Insert the budgeting calculator record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."BudgetingCalculator" ("amount", "name", "description", "frequency", "mainCategory", "subCategory", "type", "userId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (amount, name, description, frequency, mainCategory, subCategory, calc_type, postgres_user_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            budgetingcalculator_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping budgeting calculator {mongo_id} due to missing userID {userID}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Budgeting calculators migration completed{BColors.ENDC}")
    return budgetingcalculator_id_map
