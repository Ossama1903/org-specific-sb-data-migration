from BColors import BColors

def assign_permission_copies_to_template(cursor, postgres_cursor, **kwargs):
    """Assign all permission copies to the created PermissionTemplate."""
    
    print(f"{BColors.WARNING}Assigning permission copies to the created permission template...{BColors.ENDC}")
    template_id = kwargs["template_id"]
    
    # Fetch all permission copy IDs
    select_query = 'SELECT id FROM public."PermissionCopy"'
    postgres_cursor.execute(select_query)
    permission_copy_ids = [row[0] for row in postgres_cursor.fetchall()]
    
    # Insert into PermissionTemplatePermission table
    insert_query = '''
    INSERT INTO public."PermissionTemplatePermission" ("permissionId", "templateId", "permissionCopyId")
    VALUES (%s, %s, %s)
    '''
    
    for permission_copy_id in permission_copy_ids:
        data = (permission_copy_id, template_id, permission_copy_id)
        postgres_cursor.execute(insert_query, data)
    
    print(f"{BColors.OKGREEN}Permission copies assigned to permission template{BColors.ENDC}")
