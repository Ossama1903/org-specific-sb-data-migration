from BColors import BColors

def migrate_roles(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating roles...{BColors.ENDC}")
    insert_query = '''
    INSERT INTO public."Role" (name)
    VALUES (%s) RETURNING id
    '''
    roles = kwargs['roles']

    for role in roles:
        data = (role,)  # Ensure it's a tuple
        postgres_cursor.execute(insert_query, data)

    print(f"{BColors.OKGREEN}Roles migration completed{BColors.ENDC}")
