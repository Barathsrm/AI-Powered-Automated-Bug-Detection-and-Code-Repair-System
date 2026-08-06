from fastapi import APIRouter, Depends, UploadFile, File
from sqlmodel import Session

from database.database import get_session
from utils.security import get_current_user
from services.project_service import create_project_from_zip

router = APIRouter()


@router.post("/")
async def upload_project(
    file: UploadFile = File(...),
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    project = await create_project_from_zip(file, current_user.id, session)
    return {"project_id": project.id, "name": project.name}
