from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.auth import current_user
from app.db.dependencies import get_db
from app.db.models import Analysis, CV, JobOffer, MatchDetail, Recommendation, User
from app.schemas.analysis import AnalysisCreate, AnalysisResponse
from app.services.matcher import analyze

router = APIRouter(prefix="/analyses", tags=["analyses"])


def _response(analysis: Analysis, db: Session) -> AnalysisResponse:
    details = list(db.scalars(select(MatchDetail).where(MatchDetail.analysis_id == analysis.id)))
    recommendations = list(db.scalars(select(Recommendation).where(Recommendation.analysis_id == analysis.id)))
    return AnalysisResponse(id=analysis.id, cv_id=analysis.cv_id, job_offer_id=analysis.job_offer_id, score=analysis.score, skills_score=analysis.skills_score, experience_score=analysis.experience_score, education_score=analysis.education_score, keywords_score=analysis.keywords_score, explanation=analysis.explanation, matched_skills=[d.skill for d in details if d.matched], missing_skills=[d.skill for d in details if not d.matched], recommendations=[r.text for r in recommendations], created_at=analysis.created_at)


@router.post("", response_model=AnalysisResponse, status_code=201)
def create_analysis(payload: AnalysisCreate, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> AnalysisResponse:
    cv = db.scalar(select(CV).where(CV.id == payload.cv_id, CV.user_id == user.id))
    job = db.scalar(select(JobOffer).where(JobOffer.id == payload.job_offer_id, JobOffer.user_id == user.id))
    if not cv or not job:
        raise HTTPException(status_code=404, detail="CV or job offer not found")
    existing = db.scalar(select(Analysis).where(Analysis.user_id == user.id, Analysis.cv_id == payload.cv_id, Analysis.job_offer_id == payload.job_offer_id))
    if existing:
        raise HTTPException(status_code=409, detail="This CV and job offer have already been analyzed")
    result = analyze(cv.extracted_text, job.description)
    analysis = Analysis(user_id=user.id, cv_id=cv.id, job_offer_id=job.id, score=result.score, skills_score=result.skills_score, experience_score=result.experience_score, education_score=result.education_score, keywords_score=result.keywords_score, explanation=result.explanation)
    db.add(analysis)
    db.flush()
    for skill in result.matched_skills:
        db.add(MatchDetail(analysis_id=analysis.id, skill=skill, matched=True))
    for skill in result.missing_skills:
        db.add(MatchDetail(analysis_id=analysis.id, skill=skill, matched=False))
    for recommendation in result.recommendations:
        db.add(Recommendation(analysis_id=analysis.id, text=recommendation))
    db.commit()
    db.refresh(analysis)
    return _response(analysis, db)


@router.get("", response_model=list[AnalysisResponse])
def list_analyses(user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> list[AnalysisResponse]:
    return [_response(item, db) for item in db.scalars(select(Analysis).where(Analysis.user_id == user.id).order_by(Analysis.created_at.desc()))]


@router.get("/{analysis_id}", response_model=AnalysisResponse)
def get_analysis(analysis_id: int, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> AnalysisResponse:
    analysis = db.scalar(select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id))
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return _response(analysis, db)


@router.delete("/{analysis_id}", status_code=204)
def delete_analysis(analysis_id: int, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> None:
    analysis = db.scalar(select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id))
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    db.delete(analysis)
    db.commit()


@router.get("/{analysis_id}/report", response_class=StreamingResponse)
def download_report(analysis_id: int, user: Annotated[User, Depends(current_user)], db: Annotated[Session, Depends(get_db)]) -> StreamingResponse:
    analysis = db.scalar(select(Analysis).where(Analysis.id == analysis_id, Analysis.user_id == user.id))
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    result = _response(analysis, db)
    stream = BytesIO()
    pdf = canvas.Canvas(stream, pagesize=letter)
    y = 750
    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "CareerMatch AI - Compatibility Report")
    y -= 35
    pdf.setFont("Helvetica", 11)
    for line in [f"Compatibility score: {result.score}%", f"Skills component: {result.skills_score * 100:.1f}%", f"Experience component: {result.experience_score * 100:.1f}%", f"Education component: {result.education_score * 100:.1f}%", f"Keywords component: {result.keywords_score * 100:.1f}%", f"Matched skills: {', '.join(result.matched_skills) or 'None'}", f"Missing skills: {', '.join(result.missing_skills) or 'None'}"]:
        pdf.drawString(50, y, line[:110])
        y -= 20
    pdf.drawString(50, y - 5, "Recommendations:")
    y -= 25
    for recommendation in result.recommendations:
        pdf.drawString(65, y, f"- {recommendation}"[:105])
        y -= 18
    pdf.save()
    stream.seek(0)
    return StreamingResponse(stream, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=analysis-{analysis_id}.pdf"})

