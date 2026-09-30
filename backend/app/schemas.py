from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

# User Schemas
class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=6, description="Password must be at least 6 characters")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: str = Field(default="candidate", pattern="^(candidate|recruiter)$")

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# Candidate Profile Schemas
class CandidateProfileBase(BaseModel):
    headline: Optional[str] = None
    current_company: Optional[str] = None
    experience_years: float = 0.0
    skills: Optional[str] = None
    location: Optional[str] = None
    resume_url: Optional[str] = None

class CandidateProfileCreate(CandidateProfileBase):
    pass

class CandidateProfileUpdate(CandidateProfileBase):
    pass

class CandidateProfileOut(CandidateProfileBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

# Job Schemas
class JobBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=200)
    company_name: str = Field(..., min_length=2, max_length=100)
    location: str = Field(..., min_length=2, max_length=100)
    job_type: str = Field(default="Full-time", pattern="^(Full-time|Part-time|Remote|Hybrid|Contract)$")
    experience_level: str = Field(default="Mid-level (3-5 yrs)")
    min_experience: int = Field(default=0, ge=0)
    max_experience: int = Field(default=5, ge=0)
    min_salary: int = Field(default=500000, ge=0)
    max_salary: int = Field(default=1200000, ge=0)
    description: str = Field(..., min_length=10)
    requirements: str = Field(..., min_length=10)
    skills_required: str = Field(..., min_length=2)

class JobCreate(JobBase):
    pass

class JobUpdate(BaseModel):
    title: Optional[str] = None
    company_name: Optional[str] = None
    location: Optional[str] = None
    job_type: Optional[str] = None
    experience_level: Optional[str] = None
    min_experience: Optional[int] = None
    max_experience: Optional[int] = None
    min_salary: Optional[int] = None
    max_salary: Optional[int] = None
    description: Optional[str] = None
    requirements: Optional[str] = None
    skills_required: Optional[str] = None
    is_active: Optional[bool] = None

class JobOut(JobBase):
    id: int
    recruiter_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class JobListResponse(BaseModel):
    items: List[JobOut]
    total: int
    page: int
    size: int
    total_pages: int

# Application Schemas
class ApplicationCreate(BaseModel):
    job_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None

class ApplicationStatusUpdate(BaseModel):
    status: str = Field(..., pattern="^(Applied|Under Review|Shortlisted|Interview Scheduled|Rejected|Offered)$")

class ApplicationOut(BaseModel):
    id: int
    job_id: int
    candidate_id: int
    cover_letter: Optional[str] = None
    resume_url: Optional[str] = None
    status: str
    applied_at: datetime
    updated_at: Optional[datetime] = None
    job: Optional[JobOut] = None
    candidate: Optional[UserOut] = None

    class Config:
        from_attributes = True

# Saved Job Schemas
class SavedJobToggle(BaseModel):
    job_id: int

class SavedJobOut(BaseModel):
    id: int
    job_id: int
    user_id: int
    saved_at: datetime
    job: Optional[JobOut] = None

    class Config:
        from_attributes = True

# Generic Responses
class MessageResponse(BaseModel):
    message: str
    detail: Optional[str] = None
