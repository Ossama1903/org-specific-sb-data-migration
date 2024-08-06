from datetime import datetime
import pytz
from BColors import BColors

def migrate_stickball_properties_photos(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating stickball properties photos...{BColors.ENDC}")
    stickball_properties_id_map = kwargs["stickball_properties_id_map"]

    for document in cursor:
        stickball_property_id = str(document.get("_id"))
        photos = document.get("photos")
        for photo in photos:
            

            postgres_stickball_property_id = stickball_properties_id_map[stickball_property_id]
            insert_query = '''
            INSERT INTO public."StickballPropertiesPhotos" ("url", "stickballPropertiesId")
            VALUES (%s, %s) RETURNING id
            '''
            data = (photo, postgres_stickball_property_id)
            postgres_cursor.execute(insert_query, data)


    #     # Edge case for missing creation or updation time
    #     if createdAt is None or updatedAt is None:
    #         current_time = str(datetime.now(pytz.UTC)).split("+")[0]
    #         createdAt = current_time if createdAt is None else createdAt
    #         updatedAt = current_time if updatedAt is None else updatedAt


    #     # Insert the property record into the PostgreSQL database
    #     insert_query = '''
    #     INSERT INTO public."StickballProperties" ("zpid", "bedrooms", "bathrooms", "price", "yearBuild", "longitude", "latitude", "homeStatus", "description", "livingArea", "currency", "homeType", "datePostedString", "daysOnZillow", "url")
    #     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
    #     '''
    #     data = (zpid, bedrooms, bathrooms, price, yearBuilt, longitude, latitude, homeStatus, description, livingArea, currency, homeType, datePostedString, daysOnZillow, url)
    #     postgres_cursor.execute(insert_query, data)
    #     new_id = postgres_cursor.fetchone()[0]
    #     property_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}Stickball properties photos migration completed{BColors.ENDC}")
    # return property_id_map
