from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field


class ErrorRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    analysis_id: int = Field(foreign_key="analysis.id", index=True)
    error_type: str
    message: str
    stack_trace: str
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
