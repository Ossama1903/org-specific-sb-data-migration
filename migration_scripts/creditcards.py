from datetime import datetime
import pytz
from BColors import BColors

def migrate_creditcards(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating credit cards...{BColors.ENDC}")
    creditcard_id_map = {}
    user_id_map = kwargs["user_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        isBlocked = document.get("isBlocked")
        tempFreeze = document.get("tempFreeze")
        currentAmount = document.get("currentAmount")
        cardNumber = document.get("cardNumber")
        cvv = document.get("cvv")
        expiryDate = document.get("expiryDate")
        userID = str(document.get("userID"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the userID exists in the corresponding map
        if userID in user_id_map:
            postgres_user_id = user_id_map[userID]

            # Insert the credit card record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."CreditCard" ("isBlocked", "tempFreeze", "currentAmount", "cardNumber", "cvv", "expiryDate", "userId", "createdAt", "updatedAt")
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id
            '''
            data = (isBlocked, tempFreeze, currentAmount, cardNumber, cvv, expiryDate, postgres_user_id, createdAt, updatedAt)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            creditcard_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping credit card {mongo_id} due to missing userID {userID}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}Credit cards migration completed{BColors.ENDC}")
    return creditcard_id_map
