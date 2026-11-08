from sqlalchemy import Integer, String, Float, Column, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship 

Base = declarative_base() 

class ProfileModel(Base):
    __tablename__ = 'profiles'

    profile_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False, unique=True, index=True)
    major = Column(String, nullable=True)
    year = Column(String, nullable=True)
    study_hours_week = Column(Integer, nullable=True)
    session_minutes = Column(Integer, nullable=True)
    preferred_time = Column(String, nullable=True)

    meetings = relationship(
        "CourseMeetingModel",
        back_populates="profile",
        cascade="all, delete-orphan"
    )

class CourseMeetingModel(Base):
    __tablemame__ = 'course_meetings'

    meeting_id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey("profiles.profile_id", ondelete="CASCADE"), nullable=False)
    course_code = Column(String, nullable=False)
    course_name = Column(String, nullable=True)
    meeting_day = Column(String, nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)

    profile = relationship(
        "ProfileModel", 
        back_populates="meetings"
    )