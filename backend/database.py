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

        self.SessionLocal = sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self.engine
        )

        self.init_db() 

    def init_db(self):
        Base.metadata.create_all(bind=self.engine)

        with self.engine.connect() as conn: 
            conn.execute(text("PRAGMA foreign_keys = ON; "))

    def get_session(self):
        return self.SessionLocal()

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
            session.execute(text("DELETE FROM sqlite_sequence WHERE name='course_meetings';"))
            session.commit() 

db = Database() 

def get_db(): 
    session = db.get_session() 
    try: 
        yield session
    finally: 
        session.close() 
