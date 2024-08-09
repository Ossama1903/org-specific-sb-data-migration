from migrate_collection import migrate_collection
from migration_scripts.organizations import migrate_organizations
from migration_scripts.admins import migrate_admins
from migration_scripts.users import migrate_users
from migration_scripts.icons import migrate_icons
from migration_scripts.wordsGlossary import migrate_words_glossary
from migration_scripts.categories import migrate_categories
from migration_scripts.podcasts import migrate_podcasts
from migration_scripts.permissions import migrate_permissions
from migration_scripts.journals import migrate_journals
from migration_scripts.ai_request import migrate_ai_requests
from migration_scripts.notifications import migrate_notifications
from migration_scripts.modules import migrate_modules
from migration_scripts.lessons import migrate_lessons
from migration_scripts.badges import migrate_badges
from migration_scripts.lesson_badge import migrate_lesson_badges
from migration_scripts.skills import migrate_skills
from migration_scripts.amount_requests import migrate_amount_requests
from migration_scripts.stickey_assignment import migrate_stickeyassignments
from migration_scripts.stickey_assignment_users import migrate_stickeyassignmentsusers
from migration_scripts.creditcards import migrate_creditcards
from migration_scripts.transaction_histories import migrate_transactionhistories
from migration_scripts.orders import migrate_orders
from migration_scripts.products import migrate_products
from migration_scripts.lesson_words_glossaries import migrate_lessonwordsglossaries
from migration_scripts.tm_todos import migrate_tmtodos
from migration_scripts.tm_time_tracker import migrate_tmtimetracker
from migration_scripts.game_tips import migrate_gametips
from migration_scripts.grocerry_game_stocks import migrate_grocerygamestocks
from migration_scripts.money_skills import migrate_moneyskills
from migration_scripts.money_subskills import migrate_moneysubskills
from migration_scripts.money_skill_sections import migrate_moneyskillsections
from migration_scripts.prompt_categories import migrate_promptcategories
from migration_scripts.prompts import migrate_prompts
from migration_scripts.aisles import migrate_aisles
from migration_scripts.financial_goals import migrate_financialgoals
from migration_scripts.all_content import migrate_allcontents
from migration_scripts.sub_skills import migrate_subskills
from migration_scripts.skill_sections import migrate_skillsections
from migration_scripts.skill_assignments import migrate_skillassignments
from migration_scripts.enrollments import migrate_enrollments
from migration_scripts.budgeting_calculators import migrate_budgetingcalculators
from migration_scripts.quizzes import migrate_quizzes
from migration_scripts.forms import migrate_forms
from migration_scripts.analytics_settings import migrate_analyticssettings
from migration_scripts.tm_time_tracker_breaks import migrate_tmtimetrackerbreaks
from migration_scripts.form_questions import migrate_formquestions
from migration_scripts.order_items import migrate_orderitems
from migration_scripts.journal_shared_with import migrate_journal_shared_with
from migration_scripts.stickball_properties import migrate_stickballproperties
from migration_scripts.stickball_properties_address import (
    migrate_stickball_properties_address,
)
from migration_scripts.stickball_properties_photos import (
    migrate_stickball_properties_photos,
)
from migration_scripts.form_questions_options import migrate_form_questions_options
from migration_scripts.form_sections import migrate_form_sections
from migration_scripts.gc_experience import migrate_gc_experience
from migration_scripts.gc_missions import migrate_gc_missions
from migration_scripts.gc_notifications import migrate_gc_notifications
from migration_scripts.gc_participants import migrate_gc_participants
from migration_scripts.gc_submissions import migrate_gc_submissions
from migration_scripts.gc_mission_text_answers import migrate_mission_text_answers
from migration_scripts.gc_participant_member import migrate_gc_participant_members
from migration_scripts.roles import migrate_roles
from migration_scripts.permissions_copy import migrate_permission_copies
from migration_scripts.permission_template import insert_permission_template
from migration_scripts.assign_permission_template import (
    update_admins_with_permission_template,
)
from migration_scripts.assign_permission_copies_to_templates import (
    assign_permission_copies_to_template,
)

from connections import mongo_connection, postgres_connection
from migration_scripts.truncate_all_tables import truncate_all_tables


if __name__ == "__main__":
    truncate_all_tables()

    org_names_to_migrate = [
        "Workforce Readiness",
        "Brookline Bank - Eng",
        "Brookline Bank - Spa",
    ]

    migrate_collection(
        "stickballproperties",
        migrate_roles,
        roles=["Admin", "Teacher", "Mentor", "Parent"],
    )
    migrate_collection(
        "stickballproperties", migrate_permission_copies
    )

    # Updated call to migrate_collection for organizations
    org_id_map = migrate_collection(
        "organizations", migrate_organizations, org_names=org_names_to_migrate
    )

    # # #NECESSARY
    # admin_id_map = migrate_collection("admins", migrate_admins, org_id_map=org_id_map)
    # permissions_id_map = migrate_collection(
    #     "permissions", migrate_permissions, admin_id_map=admin_id_map
    # )

    # permission_template_id = migrate_collection("stickballproperties", insert_permission_template) #stickballproperties is passed just as a placeholder    # migrate_collection("stickballproperties", assign_permission_copies_to_template, template_id=permission_template_id)

    # migrate_collection("stickballproperties", update_admins_with_permission_template, admin_id_map=admin_id_map, template_id=permission_template_id)

    # gc_experience_id_map = migrate_collection(
    #     "gcexperiences", migrate_gc_experience, org_id_map=org_id_map
    # )
    # gc_mission_id_map = migrate_collection(
    #     "gcmissions", migrate_gc_missions, gc_experience_id_map=gc_experience_id_map
    # )
    # gc_notifications_id_map = migrate_collection(
    #     "gcnotifications",
    #     migrate_gc_notifications,
    #     gc_experience_id_map=gc_experience_id_map,
    # )

    # # #NECESSARY
    # # #NECESSARY
    # user_id_map = migrate_collection("users", migrate_users, org_id_map=org_id_map)
    # gc_participant_id_map = migrate_collection(
    #     "gcparticipants",
    #     migrate_gc_participants,
    #     gc_experience_id_map=gc_experience_id_map,
    #     user_id_map=user_id_map,
    # )
    # gc_submission_id_map = migrate_collection(
    #     "gcsubmissions",
    #     migrate_gc_submissions,
    #     gc_mission_id_map=gc_mission_id_map,
    #     gc_participant_id_map=gc_participant_id_map,
    # )

    # gc_mission_text_answer_id_map = migrate_collection(
    #     "gcmissions", migrate_mission_text_answers, gc_mission_id_map=gc_mission_id_map
    # )
    # gc_participant_member_id_map = migrate_collection(
    #     "gcparticipants",
    #     migrate_gc_participant_members,
    #     gc_participant_id_map=gc_participant_id_map,
    #     user_id_map=user_id_map,
    # )

    # # NOT NECESSARY
    icon_id_map = migrate_collection("icons", migrate_icons, org_id_map=org_id_map)
    # #NOT NECESSARY
    # word_glossaries_id_map = migrate_collection(
    #     "wordsglossaries", migrate_words_glossary, org_id_map=org_id_map
    # )
    # # #NECESSARY
    # categories_id_map = migrate_collection(
    #     "categories", migrate_categories, org_id_map=org_id_map
    # )
    # # #NECESSARY
    # podcasts_id_map = migrate_collection(
    #     "podcasts", migrate_podcasts, org_id_map=org_id_map
    # )

    # # #NECESSARY
    # ai_request_id_map = migrate_collection(
    #     "airequests", migrate_ai_requests, admin_id_map=admin_id_map
    # )
    # # #NECESSARY
    # notification_id_map = migrate_collection(
    #     "notifications", migrate_notifications, org_id_map=org_id_map
    # )
    # #ORG=NECESSARY ICON=NECESSARY
    module_id_map = migrate_collection(
        "modules", migrate_modules, org_id_map=org_id_map, icon_id_map=icon_id_map
    )

    # #MODULE=NECESSARY ICON=NECESSARY
    lessons_id_map = migrate_collection(
        "lessons", migrate_lessons, module_id_map=module_id_map, icon_id_map=icon_id_map
    )
    # # #ORG=NECESSARY ICON=NECESSARY
    # badges_id_map = migrate_collection(
    #     "badges", migrate_badges, org_id_map=org_id_map, icon_id_map=icon_id_map
    # )
    # # #LESSON=NECESSARY BADGE=NECESSARY
    # lesson_badge_id_map = migrate_collection(
    #     "lessonbadges",
    #     migrate_lesson_badges,
    #     lessons_id_map=lessons_id_map,
    #     badges_id_map=badges_id_map,
    # )
    # # #LESSON=NECESSARY
    # skill_id_map = migrate_collection(
    #     "skills", migrate_skills, lessons_id_map=lessons_id_map
    # )
    # # #USER=NECESSARY
    # amount_request_id_map = migrate_collection(
    #     "amountrequests", migrate_amount_requests, user_id_map=user_id_map
    # )
    # # #ORG=NECESSARY
    # stickey_assignment_id_map = migrate_collection(
    #     "stickeyassignments", migrate_stickeyassignments, org_id_map=org_id_map
    # )

    # # #BOTH NECESSARY
    # stickey_assignment_user_id_map = migrate_collection(
    #     "stickeyassignmentusers",
    #     migrate_stickeyassignmentsusers,
    #     user_id_map=user_id_map,
    #     stickey_assignment_id_map=stickey_assignment_id_map,
    # )
    # # #USER=NECESSARY
    # credit_card_id_map = migrate_collection(
    #     "creditcards", migrate_creditcards, user_id_map=user_id_map
    # )
    # # #CARD=NECESSARY
    # transaction_histories_id_map = migrate_collection(
    #     "transactionhistories",
    #     migrate_transactionhistories,
    #     card_id_map=credit_card_id_map,
    # )
    # # #CARD=NECESSARY
    # order_id_map = migrate_collection(
    #     "orders", migrate_orders, card_id_map=credit_card_id_map
    # )
    # # #PRODUCT=NECESSARY
    # product_id_map = migrate_collection(
    #     "products", migrate_products, category_id_map=categories_id_map
    # )
    # # #BOTH=NECESSARY
    # lesson_word_glossary_id_map = migrate_collection(
    #     "lessonwordsglossaries",
    #     migrate_lessonwordsglossaries,
    #     lesson_id_map=lessons_id_map,
    #     words_glossary_id_map=word_glossaries_id_map,
    # )
    # # USER=NECESSARY
    # tmtodo_id_map = migrate_collection(
    #     "tmtodos", migrate_tmtodos, user_id_map=user_id_map
    # )
    # # USER=NECESSARY
    # tmtimetracker_id_map = migrate_collection(
    #     "tmtimetrackers", migrate_tmtimetracker, user_id_map=user_id_map
    # )
    # ###
    # gametip_id_map = migrate_collection("gametips", migrate_gametips)
    # ###
    # grocerygamestock_id_map = migrate_collection(
    #     "grocerygamestocks", migrate_grocerygamestocks
    # )
    # ###
    # moneyskill_id_map = migrate_collection("moneyskills", migrate_moneyskills)

    # # MONEYSKILL=NECESSARY
    # moneysubskill_id_map = migrate_collection(
    #     "moneysubskills", migrate_moneysubskills, moneyskill_id_map=moneyskill_id_map
    # )
    # # MONEYSUBSKILL=NECESSARY
    # moneyskillsection_id_map = migrate_collection(
    #     "moneyskillsections",
    #     migrate_moneyskillsections,
    #     moneysubskill_id_map=moneysubskill_id_map,
    # )
    # ##
    # promptcategory_id_map = migrate_collection(
    #     "promptcategories", migrate_promptcategories
    # )
    # # PROMPTCATEGORY=NECESSARY
    # prompt_id_map = migrate_collection(
    #     "prompts", migrate_prompts, promptcategory_id_map=promptcategory_id_map
    # )
    # ##
    # aisle_id_map = migrate_collection("aisles", migrate_aisles)

    # # USER=NECESSARY
    # financialgoal_id_map = migrate_collection(
    #     "financialgoals", migrate_financialgoals, user_id_map=user_id_map
    # )
    # # ORG=NECESSARY
    # form_id_map = migrate_collection("forms", migrate_forms, org_id_map=org_id_map)
    # #
    # allcontent_id_map = migrate_collection(
    #     "allcontents", migrate_allcontents, form_id_map=form_id_map
    # )
    # # SKILL=NECESSARY ICON=NOT NECESSARY
    # subskill_id_map = migrate_collection(
    #     "subskills",
    #     migrate_subskills,
    #     skill_id_map=skill_id_map,
    #     icon_id_map=icon_id_map,
    # )
    # # BOTH=NECESSARY
    # skillsection_id_map = migrate_collection(
    #     "skillsections",
    #     migrate_skillsections,
    #     subskill_id_map=subskill_id_map,
    #     allcontent_id_map=allcontent_id_map,
    # )
    # # ORG=NECESSARY
    # skillassignment_id_map = migrate_collection(
    #     "skillassignments", migrate_skillassignments, org_id_map=org_id_map
    # )
    # # NO CHANGES NEEDED
    # enrollment_id_map = migrate_collection(
    #     "enrollments",
    #     migrate_enrollments,
    #     subskill_id_map=subskill_id_map,
    #     user_id_map=user_id_map,
    #     word_id_map=word_glossaries_id_map,
    #     lesson_id_map=lessons_id_map,
    #     module_id_map=module_id_map,
    #     skill_id_map=skill_id_map,
    # )

    # # USER=NECESSARY
    # budgetingcalculator_id_map = migrate_collection(
    #     "budgetingcalculators", migrate_budgetingcalculators, user_id_map=user_id_map
    # )
    # # SUBSKILL=NECESSARY ICON=NOT NECESSARY ORG=NOT NECESSARY
    # quiz_id_map = migrate_collection(
    #     "quizzes",
    #     migrate_quizzes,
    #     subskill_id_map=subskill_id_map,
    #     icon_id_map=icon_id_map,
    #     org_id_map=org_id_map,
    # )
    # # BOTH=NECESSARY
    # analyticssetting_id_map = migrate_collection(
    #     "analyticssettings",
    #     migrate_analyticssettings,
    #     org_id_map=org_id_map,
    #     form_id_map=form_id_map,
    # )
    # # NECESSARY
    # timetrackerbreak_id_map = migrate_collection(
    #     "tmtimetrackers",
    #     migrate_tmtimetrackerbreaks,
    #     tmtimetracker_id_map=tmtimetracker_id_map,
    # )
    # # NECESSARY
    # form_question_id_map = migrate_collection(
    #     "forms", migrate_formquestions, form_id_map=form_id_map
    # )
    # form_section_id_map = migrate_collection(
    #     "forms", migrate_form_sections, form_id_map=form_id_map
    # )

    # form_question_option_id_map = migrate_collection(
    #     "forms",
    #     migrate_form_questions_options,
    #     form_id_map=form_id_map,
    #     form_question_id_map=form_question_id_map,
    # )

    # # BOTH NECESSARY
    # order_items_id_map = migrate_collection(
    #     "orders",
    #     migrate_orderitems,
    #     order_id_map=order_id_map,
    #     product_id_map=product_id_map,
    # )

    # # USER=NECESSARY TEACHER=OPTIONAL
    # journal_id_map = migrate_collection(
    #     "journals",
    #     migrate_journals,
    #     user_id_map=user_id_map,
    #     teacher_id_map=admin_id_map,
    # )
    # # BOTH=NECESSARY
    # journal_shared_with_id_map = migrate_collection(
    #     "journals",
    #     migrate_journal_shared_with,
    #     user_id_map=user_id_map,
    #     journal_id_map=journal_id_map,
    # )
    # ###
    # stickball_properties_id_map = migrate_collection(
    #     "stickballproperties", migrate_stickballproperties
    # )
    # ###
    # stickball_properties_address_id_map = migrate_collection(
    #     "stickballproperties",
    #     migrate_stickball_properties_address,
    #     stickball_properties_id_map=stickball_properties_id_map,
    # )
    # ###
    # stickball_properties_photos_id_map = migrate_collection(
    #     "stickballproperties",
    #     migrate_stickball_properties_photos,
    #     stickball_properties_id_map=stickball_properties_id_map,
    # )
