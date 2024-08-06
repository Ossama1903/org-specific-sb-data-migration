from datetime import datetime
import pytz
from BColors import BColors

def migrate_orders(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating orders...{BColors.ENDC}")
    order_id_map = {}
    card_id_map = kwargs["card_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        payment_type = document.get("payment_type")
        cardnumber = document.get("cardnumber")
        totalPrice = document.get("totalPrice")
        cardID = str(document.get("cardID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the cardID exists in the corresponding map
        if cardID in card_id_map:
            postgres_card_id = card_id_map[cardID]


            # Insert the order record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."Order" ("paymentType", "cardNumber", "totalPrice", "cardId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (payment_type, cardnumber, totalPrice, postgres_card_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            order_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping order {mongo_id} due to missing cardID {cardID}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Orders migration completed{BColors.ENDC}")
    return order_id_map
