from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, select
from database import get_db 
from models import ProfileModel, CourseMeetingModel
from schemas import Profile, ProfileBase, ProfileCreate, ProfileUpdate, Year, PreferredTimeOfDay, CourseMeeting, CourseMeetingBase, CourseMeetingCreate
from typing import List
# uvicorn main:api --port 9999

api = FastAPI() 
# GET, POST, PUT, DELETE
# POST create new element
# PUT update existing element 

@api.get('/profiles/{username}', response_model=Profile)
def get_single_profile(username: str, db: Session = Depends(get_db)):
    statement = select(ProfileModel).where(ProfileModel.username == username)
    user = db.scalar(statement)

    if user is None:
        raise HTTPException(404, "User does not exist")
    return user

@api.get('/profiles', response_model=List[Profile])
def get_profiles(db: Session = Depends(get_db)):
    statement = select(ProfileModel)
    all_users = db.scalars(statement).all() 

    return all_users


@api.post('/profiles', response_model=Profile)
def create_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    already_exists = db.query(ProfileModel).filter(ProfileModel.username == profile.username).first()
    if already_exists:
        raise HTTPException(409, "Profile already exists")

    new_profile = ProfileModel(**profile.model_dump()) 
    db.add(new_profile)
    db.commit()

    return new_profile

@api.patch('/profiles/{username}', response_model=Profile)
def update_profile(username: str, profile_update: ProfileUpdate, db: Session = Depends(get_db)):
    statement = select(ProfileModel).where(ProfileModel.username == username)
    user = db.scalar(statement)

    if user is None:
        raise HTTPException(404, "User does not exist")

    update_data = profile_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
    

@api.delete('/profiles/{username}')
def delete_profile(username: str, db: Session = Depends(get_db)):

    delete_statement = select(ProfileModel).where(ProfileModel.username == username)
    deleted_profile = db.scalar(delete_statement)

    if deleted_profile is None: 
        raise HTTPException(404, "User does not exist")

    db.delete(deleted_profile)
    db.commit() 
    
    return None

@api.post('/profiles/{profile_id}/meetings', response_model=List[CourseMeeting])
def create_course_meetings(profile_id: int, meetings: List[CourseMeetingCreate], db: Session = Depends(get_db)):
    profile = db.scalar(select(ProfileModel).where(ProfileModel.profile_id == profile_id))
    if profile is None:
        raise HTTPException(404, "Profile not found")

    db_meetings = [
        CourseMeetingModel(profile_id=profile_id, **meeting.model_dump())
        for meeting in meetings
    ]

    db.add_all(db_meetings)
    db.commit()

    for m in db_meetings:
        db.refresh(m)

    return db_meetings


@api.get('/profiles/{profile_id}/meetings', response_model=List[CourseMeeting])
def get_profile_meetings(profile_id: int, db: Session = Depends(get_db)):
    profile = db.scalar(select(ProfileModel).where(ProfileModel.profile_id == profile_id))
    if profile is None:
        raise HTTPException(404, "Profile not found")

    statement = select(CourseMeetingModel).where(CourseMeetingModel.profile_id == profile_id)
    meetings = db.scalars(statement).all()
    return meetings


@api.get('/meetings', response_model=List[CourseMeeting])
def get_all_meetings(db: Session = Depends(get_db)):
    statement = select(CourseMeetingModel)
    meetings = db.scalars(statement).all()
    return meetings


@api.delete('/meetings/{meeting_id}')
def delete_course_meeting(meeting_id: int, db: Session = Depends(get_db)):
    statement = select(CourseMeetingModel).where(CourseMeetingModel.meeting_id == meeting_id)
    meeting = db.scalar(statement)

    if meeting is None:
        raise HTTPException(404, "Meeting not found")

    db.delete(meeting)
    db.commit()
    return None