from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Application, Job, User
from app.schemas import (
    ApplicationCreate, ApplicationStatusUpdate, ApplicationOut, MessageResponse
)
from app.auth import get_current_user, require_candidate, require_recruiter

router = APIRouter(prefix="/applications", tags=["Job Applications"])

@router.post("", response_model=ApplicationOut, status_code=status.HTTP_201_CREATED)
def apply_to_job(
    app_in: ApplicationCreate,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    # Check if job exists
    job = db.query(Job).filter(Job.id == app_in.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {app_in.job_id} not found"
        )
    if not job.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot apply to an inactive or closed job"
        )

    # Check for duplicate application
    existing = db.query(Application).filter(
        Application.job_id == app_in.job_id,
        Application.candidate_id == current_user.id
    ).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="You have already applied for this job"
        )

    application = Application(
        job_id=app_in.job_id,
        candidate_id=current_user.id,
        cover_letter=app_in.cover_letter,
        resume_url=app_in.resume_url,
        status="Applied"
    )
    db.add(application)
    db.commit()
    db.refresh(application)
    return application

@router.get("/my-applications", response_model=List[ApplicationOut])
def get_candidate_applications(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    return db.query(Application).filter(
        Application.candidate_id == current_user.id
    ).order_by(desc(Application.applied_at)).all()

@router.get("/job/{job_id}", response_model=List[ApplicationOut])
def get_job_applications(
    job_id: int,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    if job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only view applications for jobs you posted"
        )

    return db.query(Application).filter(
        Application.job_id == job_id
    ).order_by(desc(Application.applied_at)).all()

@router.patch("/{application_id}/status", response_model=ApplicationOut)
def update_application_status(
    application_id: int,
    status_update: ApplicationStatusUpdate,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    job = db.query(Job).filter(Job.id == application.job_id).first()
    if not job or job.recruiter_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to update applications for this job"
        )

    application.status = status_update.status
    db.commit()
    db.refresh(application)
    return application

@router.get("/{application_id}", response_model=ApplicationOut)
def get_application_details(
    application_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Application not found")

    job = db.query(Job).filter(Job.id == application.job_id).first()
    is_applicant = application.candidate_id == current_user.id
    is_job_recruiter = job and job.recruiter_id == current_user.id

    if not (is_applicant or is_job_recruiter):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access forbidden: You cannot view this application"
        )

    return application
