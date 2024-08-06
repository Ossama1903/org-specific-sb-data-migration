from datetime import datetime
import pytz
from BColors import BColors

def migrate_mission_text_answers(cursor, postgres_cursor, **kwargs):
    """Migrate gc_mission_text_answers collection to PostgreSQL."""
    
    print(f"{BColors.WARNING}Migrating GCMissionTextAnswers...{BColors.ENDC}")
    
    gc_mission_id_map = kwargs["gc_mission_id_map"]
    
    gc_mission_text_answer_id_map = {}

    for document in cursor:
        
        mission_id = str(document.get("_id"))
        textAnswers = document.get("textAnswer")


        for answer in textAnswers:
            if mission_id in gc_mission_id_map.keys():
                postgres_mission_id = gc_mission_id_map[mission_id]
                query = 'INSERT INTO public."GCMissionTextAnswer" ("answer", "gcMissionId") VALUES (%s, %s) RETURNING id'
                data = (answer, postgres_mission_id)
                postgres_cursor.execute(query, data)
            else:
                print(f"{BColors.FAIL}Skipping text_answer {answer} due to invalid missionId: {mission_id}{BColors.ENDC}")   

        

    print(f"{BColors.OKGREEN}Migration completed ✓{BColors.ENDC}")
    return gc_mission_text_answer_id_map
