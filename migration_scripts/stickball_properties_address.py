from BColors import BColors
from datetime import datetime
import pytz

def migrate_stickball_properties_address(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating StickballPropertiesAddress...{BColors.ENDC}")
    stickball_properties_id_map = kwargs["stickball_properties_id_map"]

    for document in cursor:
        stickball_properties_id = str(document.get("_id"))
        address = document.get("address")
        streetAddress = address["streetAddress"]
        city = address["city"]
        state = address["state"]
        zipCode = address["zipcode"]
        neighborhood = address["neighborhood"]
        community = address["community"]
        subdivision = address["subdivision"]

        insert_query = '''
        INSERT INTO public."StickballPropertiesAddress" ("streetAddress", "city", "state", "zipCode", "neighbourhood", "community", "subdivison", "stickballPropertiesId")
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
        '''    

        postgres_stickball_properties_id = stickball_properties_id_map[stickball_properties_id]
        data = (streetAddress, city, state, zipCode, neighborhood, community, subdivision, postgres_stickball_properties_id)
        postgres_cursor.execute(insert_query, data)


    print(f"{BColors.OKGREEN}StickballPropertiesAddress migration completed{BColors.ENDC}")
    