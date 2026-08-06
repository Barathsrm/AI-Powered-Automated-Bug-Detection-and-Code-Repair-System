from pathlib import Path


def find_requirements_file(project_path: Path) -> Path | None:
    for name in ("requirements.txt", "Pipfile", "pyproject.toml"):
        candidate = project_path / name
        if candidate.exists():
            return candidate
    return None


def install_command_for(requirements_file: Path | None) -> str:
    if requirements_file is None:
        return "echo 'no dependency file found, skipping install'"
    if requirements_file.name == "requirements.txt":
        return "pip install --no-cache-dir -r requirements.txt"
    if requirements_file.name == "pyproject.toml":
        return "pip install --no-cache-dir ."
    return "echo 'unsupported dependency file'"
