from pathlib import Path

from models.patch import Patch
from services.docker_service import run_in_sandbox
from services.error_parser import parse_errors


def validate_patch(patch: Patch, project_path: Path) -> tuple[bool, list[dict]]:
    """Applies the patch to a temp copy, reruns tests, and reports whether
    it resolved the failure and, if not, what still fails."""
    import shutil
    import subprocess
    import uuid

    temp_copy = project_path.parent / f"{project_path.name}_attempt_{uuid.uuid4().hex[:8]}"
    shutil.copytree(project_path, temp_copy)

    diff_file = temp_copy / ".patch.diff"
    diff_file.write_text(patch.diff)
    subprocess.run(["git", "apply", str(diff_file)], cwd=temp_copy, check=False)

    result = run_in_sandbox(str(temp_copy), "pytest --tb=short -q")
    remaining_errors = parse_errors(result["logs"])

    shutil.rmtree(temp_copy, ignore_errors=True)
    return (result["exit_code"] == 0, remaining_errors)
