# import sqlalchemy
# from sqlalchemy import create_engine, Integer, String, Float, Column, ForeignKey, text, func
# from sqlalchemy.orm import declarative_base, sessionmaker, relationship 
# from models import Base, ProfileModel, CourseMeetingModel
from database import Database 


db = Database() 
# db._clear_meetings_database()
# db._clear_profile_database()

db.display_all_meetings()
db.display_all_profiles()