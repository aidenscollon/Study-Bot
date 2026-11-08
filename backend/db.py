import sqlite3 
from objects import Profile, Meeting
from pathlib import Path 
import os 

from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey, text, func
from sqlalchemy.orm import declarative_base, sessionmaker, relationship 
from models import Base, ProfileModel, CourseMeetingModel

# TODO: add doc strings and type hints 

# DB_PATH = './data/app.db'


class Database(): 
    def __init__(self, db_name: str = "app.db"):
        BASE_DIR = Path(__file__).resolve().parent
        data_dir = BASE_DIR / "data"
        os.makedirs(data_dir, exist_ok=True)

        self.db_path = data_dir / db_name 
        self.db_url = f"sqlite:///{self.db_path}"

        self.engine = create_engine(
            self.db_url,
            connect_args={"check_same_thread" : False}
        )

        self.Session = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        self.init_db() 

    def init_db(self):
        Base.metadata.create_all(bind=self.engine)

        with self.engine.connect() as conn: 
            conn.exexcute(text("PRAGMA foreign_keys = ON; "))

    def get_session(self):
        return self.Session()

    def insert_profile(self, profile_data: dict):
        with self.get_session() as session: 
            db_profile = ProfileModel(**profile_data)
            session.add(db_profile)
            session.commit() 
            session.refresh(db_profile)
            return db_profile.profile_id 

    def insert_course_meetings(self, profile_id: int, courses: list[dict]):
        with self.get_session() as session: 
            db_meetings = []
            for course in courses: 
                db_meetings.append(CourseMeetingModel, **course)
            session.add_all(db_meetings)
            session.commit() 

    def display_all_profiles(self):
        with self.get_session() as session: 
            profiles = session.query(ProfileModel).all() 
            for p in profiles: 
                print((
                    p.profile_id, p.username, p.major,
                    p.year, p.study_hours_week,
                    p.session_minutes, p.preferred_time
                ))

    def display_all_meetings(self):
        with self.get_session() as session: 
            meetings = session.query(CourseMeetingModel).all() 
            for m in meetings:
                print((
                    m.meeting_id, m.profile_id, m.course_code,
                    m.course_name, m.meeting_day, m.start_time, m.end_time
                ))

    def _clear_profile_database(self):
        with self.get_session() as session: 
            session.query(ProfileModel).delete() 
            session.commit() 

            session.execute(text("DELETE FROM sqlite_sequence WHERE name='profiles';"))
            session.commit() 

    def _clear_meetings_database(self):
        with self.get_session() as session:
            session.query(CourseMeetingModel).delete() 
            session.commit() 
            session.execute(text("DETELE FROM sqlite_sequence WHERE name='course_meetings';"))
            session.commit() 

db = Database() 

def get_db(): 
    session = db.get_session() 
    try: 
        yield session
    finally: 
        session.close() 


class DB():
    def __init__(self): 
        BASE_DIR = Path(__file__).resolve().parent
        self.DB_PATH = BASE_DIR / "data" / "app.db"
        os.makedirs(f'{BASE_DIR}/data', exist_ok=True)
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