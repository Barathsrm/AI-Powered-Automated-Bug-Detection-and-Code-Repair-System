import shutil
import uuid
import zipfile
from pathlib import Path

BASE_TEMP_DIR = Path(__file__).resolve().parent.parent / "temporary_projects"


def new_project_workspace() -> Path:
    workspace = BASE_TEMP_DIR / str(uuid.uuid4())
    workspace.mkdir(parents=True, exist_ok=True)
    return workspace


def safe_extract_zip(zip_path: Path, dest: Path) -> None:
    """Extract a zip while guarding against path traversal (zip-slip)."""
    with zipfile.ZipFile(zip_path, "r") as zf:
        for member in zf.namelist():
            member_path = (dest / member).resolve()
            if not str(member_path).startswith(str(dest.resolve())):
                raise ValueError(f"Unsafe path in zip: {member}")
        zf.extractall(dest)


def cleanup_workspace(path: Path) -> None:
    shutil.rmtree(path, ignore_errors=True)
