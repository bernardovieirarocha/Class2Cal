from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import date

class Course(BaseModel):
    alias: str = Field(..., min_length=1, description="Short name/code for the course (e.g. EDO)")
    full_name: Optional[str] = Field(None, description="Complete name of the course")
    professor: Optional[str] = Field(None, description="Name of the professor")
    room: Optional[str] = Field(None, description="Classroom location")
    schedule_codes: str = Field(..., min_length=2, description="CEFET schedule codes (e.g. 24M12)")

class Semester(BaseModel):
    start_date: date
    end_date: date
    calendar_name: str = Field("Calendário Acadêmico", description="Name of the calendar")
    
    @validator('end_date')
    def end_date_must_be_after_start_date(cls, v, values):
        if 'start_date' in values and v < values['start_date']:
            raise ValueError('End date must be after start date')
        return v
