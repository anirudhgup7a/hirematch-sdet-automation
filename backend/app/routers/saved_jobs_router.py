from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import SavedJob, Job, User
from app.schemas import SavedJobToggle, SavedJobOut, MessageResponse
from app.auth import require_candidate

router = APIRouter(prefix="/saved-jobs", tags=["Saved Jobs"])

@router.post("/toggle")
def toggle_save_job(
    toggle_in: SavedJobToggle,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    job = db.query(Job).filter(Job.id == toggle_in.job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Job with ID {toggle_in.job_id} not found"
        )

    saved = db.query(SavedJob).filter(
        SavedJob.job_id == toggle_in.job_id,
        SavedJob.user_id == current_user.id
    ).first()

    if saved:
        db.delete(saved)
        db.commit()
        return {"message": "Job removed from saved list", "saved": False, "job_id": toggle_in.job_id}
    else:
        new_saved = SavedJob(job_id=toggle_in.job_id, user_id=current_user.id)
        db.add(new_saved)
        db.commit()
        return {"message": "Job saved successfully", "saved": True, "job_id": toggle_in.job_id}

@router.get("", response_model=List[SavedJobOut])
def get_saved_jobs(
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    return db.query(SavedJob).filter(
        SavedJob.user_id == current_user.id
    ).order_by(desc(SavedJob.saved_at)).all()

@router.delete("/{job_id}", response_model=MessageResponse)
def remove_saved_job(
    job_id: int,
    current_user: User = Depends(require_candidate),
    db: Session = Depends(get_db)
):
    saved = db.query(SavedJob).filter(
        SavedJob.job_id == job_id,
        SavedJob.user_id == current_user.id
    ).first()
    if not saved:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Job was not in your saved list"
        )
    db.delete(saved)
    db.commit()
    return {"message": f"Job {job_id} unsaved successfully"}
