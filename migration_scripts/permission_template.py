from BColors import BColors

def insert_permission_template(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Inserting permission_template record...{BColors.ENDC}")
    insert_query = '''
    INSERT INTO public."PermissionTemplate" ("name", "createdAt", "updatedAt", "createdById", "organizationId") 
    VALUES (%s, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, %s, %s) RETURNING id
    '''
    
    permission_template = ("full access", 1, 1)

    postgres_cursor.execute(insert_query, permission_template)
    template_id = postgres_cursor.fetchone()[0]  # Fetch the returned ID

    print(f"{BColors.OKGREEN}Permission_template record insertion completed with ID {template_id}{BColors.ENDC}")
    return template_id