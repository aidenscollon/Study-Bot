import sqlite3 
from objects import Profile, Meeting
import os 
# TODO: add doc strings and type hints 

# DB_PATH = './data/app.db'

class DB():
    def __init__(self): 
        os.makedirs('data', exist_ok=True)
        self.DB_PATH = './data/app.db'
        self.init_db() 


    def connect(self):
        conn = sqlite3.connect(self.DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.row_factory = sqlite3.Row 
        return conn 

    def init_db(self): 
        with self.connect() as conn: 
            c = conn.cursor() 
            c.execute("""CREATE TABLE IF NOT EXISTS profiles (
            profile_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            username TEXT NOT NULL UNIQUE,
            major TEXT, 
            year TEXT,
            study_hours_week INTEGER,
            session_minutes INTEGER,
            preferred_time TEXT)""")

            c.execute("""CREATE TABLE IF NOT EXISTS course_meetings (
            meeting_id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER REFERENCES profiles(profile_id) ON DELETE CASCADE, 
            course_code TEXT NOT NULL, 
            course_name TEXT,
            meeting_day TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL
            )""")

            c.execute("""CREATE INDEX IF NOT EXISTS idx_meetings_profile 
            ON course_meetings(profile_id)""")

    def insert_profile(self, profile: Profile) -> int:
        with self.connect() as conn: 
            c = conn.cursor() 
            c.execute("""INSERT INTO profiles (
            username, 
            major,
            year,
            study_hours_week,
            session_minutes,
            preferred_time) VALUES (
            :username, 
            :major, 
            :year, 
            :study_hours_week, 
            :session_minutes,
            :preferred_time)""",
            {'username' : profile.username,
            'major' : profile.major,
            'year' : profile.year,
            'study_hours_week' : profile.study_hours_week,
            'session_minutes' : profile.session_minutes,
            'preferred_time' : profile.preferred_time})
        return c.lastrowid

    def insert_course_meetings(self, profile_id: int, courses: list[dict]):
        for course in courses: 
            course['profile_id'] = profile_id
        with self.connect() as conn: 
            c = conn.cursor() 
            c.executemany("""INSERT INTO course_meetings (
            profile_id, 
            course_code, 
            course_name,
            meeting_day, 
            start_time,
            end_time) VALUES (
            :profile_id, 
            :course_code, 
            :course_name,
            :meeting_day, 
            :start_time,
            :end_time)""",
            courses)

    def display_all_profiles(self):
        with self.connect() as conn: 
            c = conn.cursor() 
            c.execute("SELECT * FROM profiles")
            rows = c.fetchall() 
        for row in rows:
            print(tuple(row))

    def display_all_meetings(self):
        with self.connect() as conn: 
            c = conn.cursor() 
            c.execute("SELECT * FROM course_meetings")
            rows = c.fetchall() 
        for row in rows: 
            print(tuple(row))

    def _clear_profile_database(self):
        with self.connect() as conn: 
            c = conn.cursor()
            try: 
                c.execute("DELETE FROM profiles;")
                c.execute("DELETE FROM sqlite_sequence WHERE name='profiles';")
            except sqlite3.OperationalError: 
                print("Table 'profiles' does not exist")

    def _clear_meetings_database(self):
        with self.connect() as conn: 
            c = conn.cursor()
            try: 
                c.execute("DELETE FROM course_meetings;")
                c.execute("DELETE FROM sqlite_sequence WHERE name='course_meetings';")
            except sqlite3.OperationalError: 
                print("Table 'course_meetings' does not exist")
