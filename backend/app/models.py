import datetime
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(255), nullable=False)
    role = Column(String(50), default="candidate", nullable=False)  # "candidate" or "recruiter"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    profile = relationship("CandidateProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    posted_jobs = relationship("Job", back_populates="recruiter", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="candidate", cascade="all, delete-orphan")
    saved_jobs = relationship("SavedJob", back_populates="user", cascade="all, delete-orphan")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    headline = Column(String(255), nullable=True)
    current_company = Column(String(255), nullable=True)
    experience_years = Column(Float, default=0.0)
    skills = Column(String(500), nullable=True)  # Comma-separated skills
    location = Column(String(100), nullable=True)
    resume_url = Column(String(500), nullable=True)

    user = relationship("User", back_populates="profile")


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    recruiter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = Column(String(255), index=True, nullable=False)
    company_name = Column(String(255), index=True, nullable=False)
    location = Column(String(100), index=True, nullable=False)
    job_type = Column(String(50), default="Full-time", nullable=False)  # "Full-time", "Remote", "Hybrid", "Part-time"
    experience_level = Column(String(50), default="Mid-level (3-5 yrs)", nullable=False)
    min_experience = Column(Integer, default=0)
    max_experience = Column(Integer, default=5)
    min_salary = Column(Integer, default=500000)  # INR (e.g. 5,00,000)
    max_salary = Column(Integer, default=1200000)
    description = Column(Text, nullable=False)
    requirements = Column(Text, nullable=False)
    skills_required = Column(String(500), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    recruiter = relationship("User", back_populates="posted_jobs")
    applications = relationship("Application", back_populates="job", cascade="all, delete-orphan")
    saved_by_users = relationship("SavedJob", back_populates="job", cascade="all, delete-orphan")


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("job_id", "candidate_id", name="uq_job_candidate_application"),
    )

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    candidate_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    cover_letter = Column(Text, nullable=True)
    resume_url = Column(String(500), nullable=True)
    status = Column(String(50), default="Applied", nullable=False)  # "Applied", "Under Review", "Shortlisted", "Interview Scheduled", "Rejected", "Offered"
    applied_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="applications")
    candidate = relationship("User", back_populates="applications")


class SavedJob(Base):
    __tablename__ = "saved_jobs"
    __table_args__ = (
        UniqueConstraint("job_id", "user_id", name="uq_job_user_saved"),
    )

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    saved_at = Column(DateTime, default=datetime.datetime.utcnow)

    # Relationships
    job = relationship("Job", back_populates="saved_by_users")
    user = relationship("User", back_populates="saved_jobs")
