from BColors import BColors

def update_admins_with_permission_template(cursor, postgres_cursor, **kwargs):
    """Update admins with the permissionTemplateId."""
    
    print(f"{BColors.WARNING}Updating admins with permissionTemplateId...{BColors.ENDC}")
    admin_id_map = kwargs["admin_id_map"]
    template_id = kwargs["template_id"]
    
    for admin_id in admin_id_map.values():
        update_query = '''
        UPDATE public."Admin"
        SET "permissionTemplateId" = %s
        WHERE id = %s
        '''
        data = (template_id, admin_id)
        postgres_cursor.execute(update_query, data)
    
    print(f"{BColors.OKGREEN}Admins updated with permissionTemplateId{BColors.ENDC}")