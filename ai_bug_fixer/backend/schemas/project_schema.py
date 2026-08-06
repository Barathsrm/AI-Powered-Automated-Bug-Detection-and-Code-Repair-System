from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ProjectRead(BaseModel):
    id: int
    name: str
    framework: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True
