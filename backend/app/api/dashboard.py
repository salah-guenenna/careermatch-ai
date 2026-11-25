from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.api.auth import current_user
from app.db.dependencies import get_db
from app.db.models import Analysis, CV, JobOffer, User

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats")
def stats(user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> dict[str, float | int | None]:
    total = db.scalar(select(func.count(Analysis.id)).where(Analysis.user_id == user.id)) or 0
    average = db.scalar(select(func.avg(Analysis.score)).where(Analysis.user_id == user.id))
    return {"cv_count": db.scalar(select(func.count(CV.id)).where(CV.user_id == user.id)) or 0, "job_count": db.scalar(select(func.count(JobOffer.id)).where(JobOffer.user_id == user.id)) or 0, "analysis_count": total, "average_score": round(float(average), 2) if average is not None else None}

