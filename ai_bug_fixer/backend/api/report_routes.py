from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlmodel import Session, select

from database.database import get_session
from utils.security import get_current_user
from models.report import Report
from schemas.report_schema import ReportRead

router = APIRouter()


@router.get("/{analysis_id}", response_model=ReportRead)
def get_report(
    analysis_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    report = session.exec(
        select(Report).where(Report.analysis_id == analysis_id)
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report


@router.get("/{analysis_id}/download")
def download_report(
    analysis_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    report = session.exec(
        select(Report).where(Report.analysis_id == analysis_id)
    ).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return FileResponse(report.file_path, filename=f"report_{analysis_id}.pdf")
