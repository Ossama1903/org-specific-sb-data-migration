from datetime import datetime
import pytz
from BColors import BColors

def migrate_transactionhistories(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating transaction histories...{BColors.ENDC}")
    transaction_history_id_map = {}
    card_id_map = kwargs["card_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        transactionType = document.get("transactionType")
        amount = document.get("amount")
        description = document.get("description")
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


            # Insert the transaction history record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."TransactionHistory" ("transactionType", "amount", "description", "cardId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (transactionType, amount, description, postgres_card_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            transaction_history_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping transaction history {mongo_id} due to missing cardID {cardID}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Transaction histories migration completed{BColors.ENDC}")
    return transaction_history_id_map
