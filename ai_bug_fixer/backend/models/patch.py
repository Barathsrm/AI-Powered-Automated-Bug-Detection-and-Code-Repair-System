from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class Patch(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int = Field(foreign_key="analysis.id", index=True)
    attempt_number: int
    file_path: str
    diff: str
    explanation: str
    confidence_score: Optional[float] = None
    applied: bool = Field(default=False)
    validated: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
