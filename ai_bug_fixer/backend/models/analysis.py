from typing import Optional
from datetime import datetime
from enum import Enum
from sqlmodel import SQLModel, Field


class AnalysisStatus(str, Enum):
    queued = "queued"
    running = "running"
    repairing = "repairing"
    validating = "validating"
    success = "success"
    failed = "failed"


class Analysis(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    project_id: int = Field(foreign_key="project.id", index=True)
    status: AnalysisStatus = Field(default=AnalysisStatus.queued)
    attempt_count: int = Field(default=0)
    max_attempts: int = Field(default=3)
    tokens_used: int = Field(default=0)
    token_budget: int = Field(default=50_000)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
