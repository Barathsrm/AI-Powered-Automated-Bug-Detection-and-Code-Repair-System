from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from utils.security import get_current_user
from models.analysis import Analysis
from schemas.analysis_schema import AnalysisCreate, AnalysisRead
from services.execution_service import queue_analysis

router = APIRouter()


@router.post("/", response_model=AnalysisRead)
def start_analysis(
    payload: AnalysisCreate,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    # Creates the Analysis row as "queued" and hands off to a background
    # worker (see services/execution_service.py) instead of blocking here -
    # a full run (docker build + tests + AI round trips) can take minutes.
    analysis = queue_analysis(payload.project_id, session)
    return analysis


@router.get("/{analysis_id}", response_model=AnalysisRead)
def get_analysis_status(
    analysis_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    analysis = session.get(Analysis, analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
