from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, desc, asc
from app.database import get_db
from app.models import Job, User, Application
from app.schemas import JobCreate, JobUpdate, JobOut, JobListResponse, MessageResponse
from app.auth import get_current_user, require_recruiter

router = APIRouter(prefix="/jobs", tags=["Jobs"])

@router.get("", response_model=JobListResponse)
def list_jobs(
    keyword: Optional[str] = Query(None, description="Search keyword in title, company, skills or description"),
    location: Optional[str] = Query(None, description="Filter by location"),
    job_type: Optional[str] = Query(None, description="Full-time, Remote, Hybrid, Part-time, Contract"),
    experience_level: Optional[str] = Query(None, description="Experience level filter"),
    min_salary: Optional[int] = Query(None, description="Minimum salary expectation (INR)"),
    sort_by: str = Query("newest", description="Sorting: newest, salary_desc, salary_asc, experience"),
    page: int = Query(1, ge=1, description="Page number"),
    size: int = Query(10, ge=1, le=100, description="Page size"),
    is_active_only: bool = Query(True, description="Filter active jobs only"),
    db: Session = Depends(get_db)
):
    query = db.query(Job)
    if is_active_only:
        query = query.filter(Job.is_active == True)

    if keyword:
        term = f"%{keyword.strip()}%"
        query = query.filter(
            or_(
                Job.title.ilike(term),
                Job.company_name.ilike(term),
                Job.skills_required.ilike(term),
                Job.description.ilike(term),
                Job.location.ilike(term)
            )
        )

    if location:
        query = query.filter(Job.location.ilike(f"%{location.strip()}%"))

    if job_type:
        query = query.filter(Job.job_type == job_type)

    if experience_level:
        query = query.filter(Job.experience_level.ilike(f"%{experience_level.strip()}%"))

    if min_salary is not None:
        query = query.filter(Job.max_salary >= min_salary)

    # Sorting
    if sort_by == "salary_desc":
        query = query.order_by(desc(Job.max_salary))
    elif sort_by == "salary_asc":
        query = query.order_by(asc(Job.min_salary))
    elif sort_by == "experience":
        query = query.order_by(asc(Job.min_experience))
    else:  # newest
        query = query.order_by(desc(Job.created_at))

    total = query.count()
    total_pages = (total + size - 1) // size if total > 0 else 1
    items = query.offset((page - 1) * size).limit(size).all()

    return {
        "items": items,
        "total": total,
        "page": page,
        "size": size,
        "total_pages": total_pages
    }

@router.get("/search/suggestions", response_model=List[str])
def get_search_suggestions(
    q: str = Query(..., min_length=1, description="Search term for suggestions"),
    db: Session = Depends(get_db)
):
    term = f"%{q.strip()}%"
    jobs = db.query(Job).filter(
        Job.is_active == True,
        or_(Job.title.ilike(term), Job.skills_required.ilike(term), Job.company_name.ilike(term))
    ).limit(10).all()

    suggestions = set()
    for job in jobs:
        if q.lower() in job.title.lower():
            suggestions.add(job.title)
        if q.lower() in job.company_name.lower():
            suggestions.add(job.company_name)
        for skill in job.skills_required.split(","):
            skill = skill.strip()
            if q.lower() in skill.lower():
                suggestions.add(skill)

    return sorted(list(suggestions))[:8]

@router.get("/recruiter/my-jobs", response_model=List[JobOut])
def get_recruiter_jobs(
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    return db.query(Job).filter(Job.recruiter_id == current_user.id).order_by(desc(Job.created_at)).all()

@router.get("/{job_id}", response_model=JobOut)
def get_job_by_id(job_id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")
    return job

@router.post("", response_model=JobOut, status_code=status.HTTP_201_CREATED)
def create_job(
    job_in: JobCreate,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    job = Job(
        **job_in.model_dump(),
        recruiter_id=current_user.id,
        is_active=True
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return job

@router.put("/{job_id}", response_model=JobOut)
def update_job(
    job_id: int,
    job_in: JobUpdate,
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to modify this job")

    update_data = job_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(job, field, value)

    db.commit()
    db.refresh(job)
    return job

@router.delete("/{job_id}", response_model=MessageResponse)
def delete_or_deactivate_job(
    job_id: int,
    hard_delete: bool = Query(False, description="If true, permanently delete from DB; otherwise mark inactive"),
    current_user: User = Depends(require_recruiter),
    db: Session = Depends(get_db)
):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Job with ID {job_id} not found")
    if job.recruiter_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have permission to delete this job")

    if hard_delete:
        db.delete(job)
        db.commit()
        return {"message": f"Job {job_id} permanently deleted"}
    else:
        job.is_active = False
        db.commit()
        return {"message": f"Job {job_id} marked as inactive"}
