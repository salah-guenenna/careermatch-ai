from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class AnalysisCreate(BaseModel):
    cv_id: int = Field(gt=0)
    job_offer_id: int = Field(gt=0)


class AnalysisResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    cv_id: int
    job_offer_id: int
    score: float
    skills_score: float
    experience_score: float
    education_score: float
    keywords_score: float
    explanation: str
    matched_skills: list[str]
    missing_skills: list[str]
    recommendations: list[str]
    created_at: datetime

