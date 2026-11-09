from typing import List, Optional
from enum import IntEnum 
from pydantic import BaseModel, Field, ConfigDict

class PreferredTimeOfDay(IntEnum):
    MORNING = 1
    AFTERNOON = 2
    EVENING = 3 
    NIGHT = 4

class Year(IntEnum):
    FRESHMAN = 1
    SOPHOMORE = 2
    JUNIOR = 3
    SENIOR = 4
    GRADUATE = 5 

class ProfileBase(BaseModel):
    username: str = Field(..., description='Profile username')
    major: str = Field(..., description='User major')
    year: Year = Field(..., description='Year of student (Freshman, Sophomore, Junior, Senior, Graduate)')
    study_hours_week: int = Field(..., description='Preferred number of study hours per week')
    session_minutes: int = Field(..., description='Preferred number of minutes per study session')
    preferred_time: PreferredTimeOfDay = Field(..., description='Preferred time to study (Morning, Afternoon, Evening, Night)')

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class ProfileCreate(ProfileBase):
    pass 

class Profile(ProfileBase):
    profile_id: int = Field(..., description='Unique identifier of a profile')

class ProfileUpdate(BaseModel):
    username: Optional[str] = Field(None, description='Profile username')
    major: Optional[str] = Field(None, description='User major')
    year: Optional[Year] = Field(None, description='Year of student (Freshman, Sophomore, Junior, Senior, Graduate)')
    study_hours_week: Optional[int] = Field(None, description='Preferred number of study hours per week')
    session_minutes: Optional[int] = Field(None, description='Preferred number of minutes per study session')
    preferred_time: Optional[PreferredTimeOfDay] = Field(None, description='Preferred time to study (Morning, Afternoon, Evening, Night)')
    
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

class CourseMeetingBase(BaseModel):
    course_code: str = Field(..., description="Course code")
    course_name: Optional[str] = Field(None, description="Full name of the course")
    meeting_day: str = Field(..., description="Day of the week (Mon, Tue...)")
    start_time: str = Field(..., description="Start time (ex: 10:00)")
    end_time: str = Field(..., description="End time (ex: 13:30)")

class CourseMeetingCreate(CourseMeetingBase):
    pass

class CourseMeeting(CourseMeetingBase):
    meeting_id: int = Field(..., description="Unique identifier for the meeting")
    profile_id: int = Field(..., description="Foreign key linking to the profile")

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)