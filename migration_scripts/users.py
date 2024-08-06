from datetime import datetime
import pytz

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def migrate_users(cursor, postgres_cursor, **kwargs):
    """Migrate users collection to PostgreSQL."""
    
    print(f"{bcolors.WARNING}Migrating users...{bcolors.ENDC}")
    org_id_map = kwargs["org_id_map"]
    user_id_map = {}
    for document in cursor:
        mongo_id = document.get("_id")
        email = document.get("email")
        firstname = document.get("firstName")
        lastname = document.get("lastName")
        confirmed = document.get("confirmed")
        photo = document.get("photo")
        blocked = document.get("blocked")
        phoneNumber = document.get("phoneNumber")
        code = document.get("code")
        createdAt = document.get("createdAt")
        updatedAt = document.get("updatedAt")
        confirmationToken = document.get("confirmationToken")
        dob = document.get("dob")
        password = document.get("password")
        zipCode = document.get("zipCode")
        organizationId = str(document.get("OrganizationId"))
        create_transaction_details = document.get("create_transaction_details")
        reset_password_token = document.get("reset_password_token")
        isClever = document.get("isClever")
        userClass = document.get("class")
        cleverID = document.get("cleverID")
        districtID = document.get("districtID")
        teacher = document.get("teacher")

        
        if firstname == None:
            firstname = ""
        
        # Edge case for missing creation or updation time
        if createdAt == None or updatedAt == None:
            createdAt = str(datetime.now(pytz.UTC)).split("+")[0]
            updatedAt = str(datetime.now(pytz.UTC)).split("+")[0]

        # Check if the email already exists in the database
        check_query = 'SELECT EXISTS(SELECT 1 FROM public."User" WHERE email = %s)'
        postgres_cursor.execute(check_query, (email,))
        if postgres_cursor.fetchone()[0]:
            print(f"{bcolors.FAIL}Skipping already migrated email:{bcolors.ENDC} {email}")
            continue

        # Edge case for users having no organization: Any user with no organization is ignored.
        if str(organizationId) in org_id_map.keys():
            org_id_to_assign = org_id_map[organizationId]
            query = 'INSERT INTO public."User" ("email", "dob", "phoneNumber", "zipCode", "password", "firstName", "lastName", "resetPasswordToken", "confirmationToken", "confirmed", "blocked", "photo", "code", "isClever", "cleverID", "districtID", "class", "teacher", "createdAt", "updatedAt", "create_transaction_details", "organizationId" ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id'
            data = (email, dob, phoneNumber, zipCode, password, firstname, lastname, reset_password_token, confirmationToken, confirmed,blocked, photo, code, isClever, cleverID, districtID, userClass, teacher, createdAt, updatedAt, create_transaction_details, org_id_to_assign)
            postgres_cursor.execute(query, data)
            new_id = postgres_cursor.fetchone()[0]
            user_id_map[str(mongo_id)] = new_id

    print(f"{bcolors.OKGREEN}Users migration completed{bcolors.ENDC}")
    return user_id_map
