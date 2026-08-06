from pathlib import Path

MARKERS = {
    "django": ["manage.py"],
    "flask": ["app.py", "wsgi.py"],
    "fastapi": ["main.py"],
    "generic": ["requirements.txt", "pyproject.toml"],
}


def detect_framework(project_path: Path) -> str:
    files = {p.name for p in project_path.rglob("*") if p.is_file()}
    for framework, markers in MARKERS.items():
        if any(marker in files for marker in markers):
            return framework
    return "unknown"
