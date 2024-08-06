from datetime import datetime
import pytz
from BColors import BColors

def migrate_grocerygamestocks(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating grocery game stocks...{BColors.ENDC}")
    grocerygamestock_id_map = {}

    for document in cursor:
        mongo_id = str(document.get("_id"))
        shareName = document.get("shareName")
        sharePrice = document.get("sharePrice")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt


        # Insert the grocery game stock record into the PostgreSQL database
        insert_query = '''
        INSERT INTO public."GroceryGameStock" ("shareName", "sharePrice", "createdAt", "updatedAt")
        VALUES (%s, %s, %s, %s) RETURNING id
        '''
        data = (shareName, sharePrice, createdAt, updatedAt)
        postgres_cursor.execute(insert_query, data)
        new_id = postgres_cursor.fetchone()[0]
        grocerygamestock_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}Grocery game stocks migration completed{BColors.ENDC}")
    return grocerygamestock_id_map
