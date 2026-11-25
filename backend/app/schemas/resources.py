from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CVResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    filename: str
    created_at: datetime


class JobCreate(BaseModel):
    title: str = Field(min_length=1, max_length=200)
    company: str | None = Field(default=None, max_length=200)
    description: str = Field(min_length=20)


class JobResponse(JobCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime

