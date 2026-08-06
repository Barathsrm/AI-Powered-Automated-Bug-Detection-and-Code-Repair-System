from pydantic import BaseModel
from datetime import datetime


class ReportRead(BaseModel):
    id: int
    analysis_id: int
    summary: str
    created_at: datetime

    class Config:
        from_attributes = True
