# WITH AdminRoleId AS (
#     SELECT id
#     FROM public."Role"
#     WHERE name = 'Admin'
# )

# INSERT INTO public."AdminRole" ("adminId", "roleId")
# SELECT a.id, ar.id
# FROM public."Admin" a, AdminRoleId ar
# ON CONFLICT ("adminId", "roleId") DO NOTHING;