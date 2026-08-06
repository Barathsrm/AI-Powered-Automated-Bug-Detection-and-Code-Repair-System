from pathlib import Path
from fastapi import UploadFile
from sqlmodel import Session

from models.project import Project
from utils.file_utils import new_project_workspace, safe_extract_zip
from services.framework_detector import detect_framework


async def create_project_from_zip(file: UploadFile, user_id: int, session: Session) -> Project:
    workspace = new_project_workspace()
    zip_path = workspace / "upload.zip"

    with open(zip_path, "wb") as f:
        f.write(await file.read())

    safe_extract_zip(zip_path, workspace)
    zip_path.unlink(missing_ok=True)

    framework = detect_framework(workspace)

    project = Project(
        user_id=user_id,
        name=file.filename or "uploaded_project",
        storage_path=str(workspace),
        framework=framework,
    )
    session.add(project)
    session.commit()
    session.refresh(project)
    return project
