from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from database.database import get_session
from utils.security import get_current_user
from models.patch import Patch
from schemas.patch_schema import PatchRead

router = APIRouter()


@router.get("/{analysis_id}/patches", response_model=list[PatchRead])
def list_patches(
    analysis_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return session.exec(
        select(Patch).where(Patch.analysis_id == analysis_id)
    ).all()


@router.post("/{patch_id}/approve")
def approve_patch(
    patch_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    patch = session.get(Patch, patch_id)
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    patch.applied = True
    session.add(patch)
    session.commit()
    return {"status": "approved"}


@router.post("/{patch_id}/reject")
def reject_patch(
    patch_id: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    patch = session.get(Patch, patch_id)
    if not patch:
        raise HTTPException(status_code=404, detail="Patch not found")
    patch.applied = False
    session.add(patch)
    session.commit()
    return {"status": "rejected"}
