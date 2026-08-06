from pydantic import BaseModel
from typing import Optional


class PatchRead(BaseModel):
    id: int
    file_path: str
    diff: str
    explanation: str
    confidence_score: Optional[float]
    applied: bool
    validated: bool

    class Config:
        from_attributes = True
