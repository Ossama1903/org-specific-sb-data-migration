from datetime import datetime
import pytz
from BColors import BColors

def migrate_stickballproperties(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating stickball properties...{BColors.ENDC}")
    property_id_map = {}

    for document in cursor:
        mongo_id = str(document.get("_id"))
        zpid = document.get("zpid")
        bedrooms = document.get("bedrooms")
        bathrooms = document.get("bathrooms")
        price = document.get("price")
        yearBuilt = document.get("yearBuilt")
        longitude = document.get("longitude")
        latitude = document.get("latitude")
        homeStatus = document.get("homeStatus")
        description = document.get("description")
        livingArea = document.get("livingArea")
        currency = document.get("currency")
        homeType = document.get("homeType")
        datePostedString = document.get("datePostedString")
        daysOnZillow = document.get("daysOnZillow")
        url = document.get("url")
        createdAt = document.get("createdAt", str(datetime.now(pytz.UTC)).split("+")[0])
        updatedAt = document.get("updatedAt", str(datetime.now(pytz.UTC)).split("+")[0])

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt


        # Insert the property record into the PostgreSQL database
        insert_query = '''
        INSERT INTO public."StickballProperties" ("zpid", "bedrooms", "bathrooms", "price", "yearBuild", "longitude", "latitude", "homeStatus", "description", "livingArea", "currency", "homeType", "datePostedString", "daysOnZillow", "url")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        '''
        data = (zpid, bedrooms, bathrooms, price, yearBuilt, longitude, latitude, homeStatus, description, livingArea, currency, homeType, datePostedString, daysOnZillow, url)
        postgres_cursor.execute(insert_query, data)
        new_id = postgres_cursor.fetchone()[0]
        property_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}Stickball properties migration completed{BColors.ENDC}")
    return property_id_map
