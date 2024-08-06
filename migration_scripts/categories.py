from datetime import datetime
import pytz
from BColors import BColors

def migrate_categories(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating categories...{BColors.ENDC}")
    category_id_map = {}
    org_id_map = kwargs["org_id_map"]
    for document in cursor:
        mongo_id = document.get("_id")
        name = document.get("name")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        organizationId = document.get("OrganizationId")
        
        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        if str(organizationId) in org_id_map:
            org_id_to_assign = org_id_map[str(organizationId)]
            insert_query = 'INSERT INTO public."Category" ("name", "organizationId", "createdAt", "updatedAt") VALUES (%s, %s, %s, %s) RETURNING id'
            data = (name, org_id_to_assign, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            category_id_map[str(mongo_id)] = new_id
        else: 
            print(f"{BColors.FAIL}Skipping category {str(mongo_id)} because it isn't associated to an organization{BColors.ENDC}")


    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return category_id_map
