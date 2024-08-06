from datetime import datetime
import pytz
from BColors import BColors

def migrate_tmtodos(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating tmtodos...{BColors.ENDC}")
    tmtodo_id_map = {}
    user_id_map = kwargs["user_id_map"]

    for document in cursor:
        mongo_id = str(document.get("_id"))
        title = document.get("title")
        priorityIndex = document.get("priorityIndex")
        user = str(document.get("user"))
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")

        # Edge case for missing creation or updation time
        if createdAt is None or updatedAt is None:
            current_time = str(datetime.now(pytz.UTC)).split("+")[0]
            createdAt = current_time if createdAt is None else createdAt
            updatedAt = current_time if updatedAt is None else updatedAt

        # Check if the user exists in the corresponding map
        if user in user_id_map:
            postgres_user_id = user_id_map[user]

            # Insert the tmtodo record into the PostgreSQL database
            insert_query = '''
            INSERT INTO public."TMTodo" ("title", "priorityIndex", "user_id")
            VALUES (%s, %s, %s) RETURNING id
            '''
            data = (title, priorityIndex, postgres_user_id)
            postgres_cursor.execute(insert_query, data)
            new_id = postgres_cursor.fetchone()[0]
            tmtodo_id_map[mongo_id] = new_id
        else:
            print(f"{BColors.FAIL}Skipping tmtodo {mongo_id} due to missing user {user}{BColors.ENDC}")

    print(f"{BColors.OKGREEN}TMTodos migration completed{BColors.ENDC}")
    return tmtodo_id_map
