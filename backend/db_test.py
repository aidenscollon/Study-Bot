import db 
from objects import Profile 
import os 

db = db.DB() 
db._clear_profile_database() 
db._clear_meetings_database()

profclass = Profile(
    'user1',
    'data science',
    'senior',
    10,
    45,
    'afternoon'
)
db.insert_profile(profclass)

courses = [{'course_code': 'CIS 4626',
            'course_name': 'Intro to Deep Learning',
            'meeting_day' : 'Tue',
            'start_time' : '12:30',
            'end_time' : '13:45'},
            {'course_code': 'CIS 4626',
            'course_name': 'Intro to Deep Learning',
            'meeting_day' : 'Thu',
            'start_time' : '12:30',
            'end_time' : '13:45'},]

db.insert_course_meetings(1, courses)


# prof1 = {
#     'username': 'user1',
#     'major' : 'data science',
#     'year' : 'senior',
#     'study_hours_week' : 10,
#     'session_minutes' : 45,
#     'preferred_time' : 'afternoon'
# }
# prof2 = {
#     'username': 'user2',
#     'major' : 'computer science',
#     'year' : 'sophomore',
#     'study_hours_week' : 5,
#     'session_minutes' : 30,
#     'preferred_time' : 'evening'
# }
# prof3 = {
#     'username': 'user3',
#     'major' : 'environmental science',
#     'year' : 'freshman',
#     'study_hours_week' : 20,
#     'session_minutes' : 120,
#     'preferred_time' : 'morning'
# }

# profs = [prof1, prof2, prof3]

# for prof in profs: 
#     db.insert_profile(prof)

db.display_all_profiles() 
db.display_all_meetings()

