from pydantic import BaseModel
from datetime import datetime


class AnalysisCreate(BaseModel):
    project_id: int


class AnalysisRead(BaseModel):
    id: int
    project_id: int
    status: str
    attempt_count: int
    max_attempts: int
    tokens_used: int
    updated_at: datetime

    class Config:
        from_attributes = True
