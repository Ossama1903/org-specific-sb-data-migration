from BColors import BColors
from datetime import datetime
import pytz

def migrate_orderitems(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating order items...{BColors.ENDC}")
    form_question_id_map = {}
    order_id_map = kwargs["order_id_map"]
    product_id_map = kwargs["product_id_map"]


    for document in cursor:
        order_id = str(document.get("_id"))
        items = document.get("items")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        for item in items:
            quantity = item.get("qty")
            productId = str(item.get("productId"))
            mongo_id = item.get("_id")
            order_id
            print()
        
            insert_query = '''
            INSERT INTO public."OrderItem" ("qty", "orderId", "productId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s) RETURNING id
            '''    

            postgres_order_id = order_id_map[order_id]
            postgres_product_id = product_id_map[productId]

            data = (quantity, postgres_order_id, postgres_product_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            form_question_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}OrderItems migration completed{BColors.ENDC}")
    return form_question_id_map
    