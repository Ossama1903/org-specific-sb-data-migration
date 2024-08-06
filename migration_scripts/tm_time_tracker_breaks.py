from datetime import datetime
import pytz
from BColors import BColors

def migrate_tmtimetrackerbreaks(cursor, postgres_cursor, **kwargs):
    print(f"{BColors.WARNING}Migrating time tracker breaks...{BColors.ENDC}")
    timetrackerbreak_id_map = {}
    tmtimetracker_id_map = kwargs["tmtimetracker_id_map"]
    for document in cursor:
        tracker_id = str(document.get("_id"))
        time_tracker_breaks = document.get("breaks")
        if tracker_id not in tmtimetracker_id_map:
            print(f"{BColors.FAIL}Skipping time tracker breaks for tracker_id {tracker_id} because it doesn't exist in tmtimetracker_id_map{BColors.ENDC}")
            continue
        
        for tracker_break in time_tracker_breaks:
            if tracker_break:
                mongo_id = tracker_break["_id"]
                start_time = tracker_break["start"]
                end_time = tracker_break["end"]
                postgres_tracker_id = tmtimetracker_id_map[tracker_id]

                insert_query = '''
                INSERT INTO public."TMTimeTrackerBreak" ("start", "end", "tmTimeTrackerId")
                VALUES (%s, %s, %s) RETURNING id
                '''         

                data = (start_time, end_time, postgres_tracker_id)
                postgres_cursor.execute(insert_query, data)
                new_id = postgres_cursor.fetchone()[0]
                timetrackerbreak_id_map[mongo_id] = new_id

    print(f"{BColors.OKGREEN}TMTimeTrackerBreaks migration completed ✓{BColors.ENDC}")
    return timetrackerbreak_id_map
