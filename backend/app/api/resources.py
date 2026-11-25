from pathlib import Path
from typing import Annotated
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import current_user
from app.db.dependencies import get_db
from app.db.models import CV, JobOffer, User
from app.schemas.resources import CVResponse, JobCreate, JobResponse
from app.services.pdf_extractor import UnsupportedDocumentError, extract_pdf_text

router = APIRouter(tags=["CVs and jobs"])
UPLOAD_DIR = Path("uploads")
MAX_FILE_SIZE = 5 * 1024 * 1024


@router.post("/cvs/upload", response_model=CVResponse, status_code=201)
async def upload_cv(user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)], file: UploadFile = File(...)) -> CV:
    if file.content_type != "application/pdf" or not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Only PDF files are accepted")
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=413, detail="PDF exceeds the 5 MB limit")
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    path = UPLOAD_DIR / f"{user.id}-{uuid4().hex}.pdf"
    path.write_bytes(content)
    try:
        text = extract_pdf_text(path)
    except UnsupportedDocumentError as exc:
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    duplicate = db.scalar(select(CV).where(CV.user_id == user.id, CV.filename == file.filename, CV.extracted_text == text))
    if duplicate:
        path.unlink(missing_ok=True)
        raise HTTPException(status_code=409, detail="This CV is already uploaded")
    cv = CV(user_id=user.id, filename=file.filename, storage_path=str(path), extracted_text=text)
    db.add(cv)
    db.commit()
    db.refresh(cv)
    return cv


@router.get("/cvs", response_model=list[CVResponse])
def list_cvs(user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> list[CV]:
    return list(db.scalars(select(CV).where(CV.user_id == user.id).order_by(CV.created_at.desc())))


@router.delete("/cvs/{cv_id}", status_code=204)
def delete_cv(cv_id: int, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> None:
    cv = db.scalar(select(CV).where(CV.id == cv_id, CV.user_id == user.id))
    if not cv:
        raise HTTPException(status_code=404, detail="CV not found")
    Path(cv.storage_path).unlink(missing_ok=True)
    db.delete(cv)
    db.commit()


@router.post("/jobs", response_model=JobResponse, status_code=201)
def create_job(payload: JobCreate, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> JobOffer:
    duplicate = db.scalar(select(JobOffer).where(JobOffer.user_id == user.id, JobOffer.title == payload.title, JobOffer.company == payload.company, JobOffer.description == payload.description))
    if duplicate:
        raise HTTPException(status_code=409, detail="This job offer already exists")
    job = JobOffer(user_id=user.id, **payload.model_dump())
    db.add(job)
    db.commit()
    db.refresh(job)
    return job


@router.get("/jobs", response_model=list[JobResponse])
def list_jobs(user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> list[JobOffer]:
    return list(db.scalars(select(JobOffer).where(JobOffer.user_id == user.id).order_by(JobOffer.created_at.desc())))


@router.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: int, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> None:
    job = db.scalar(select(JobOffer).where(JobOffer.id == job_id, JobOffer.user_id == user.id))
    if not job:
        raise HTTPException(status_code=404, detail="Job offer not found")
    db.delete(job)
    db.commit()

