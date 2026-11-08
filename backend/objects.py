class Profile():
    def __init__(self, username: str, major: str, year: str, study_hours_week: int, session_minutes: int, preferred_time: str):
        self.username = username
        self.major = major
        self.year = year
        self.study_hours_week = study_hours_week
        self.session_minutes = session_minutes
        self.preferred_time = preferred_time

class Meeting(): 
    def __init__(self, course_code: str, course_name: str, meeting_day: str, start_time: str, end_time: str):
        self.course_code = course_code
        self.course_name = course_name 
        self.meeting_day = meeting_day 
        self.start_time = start_time
        self.end_time = end_time