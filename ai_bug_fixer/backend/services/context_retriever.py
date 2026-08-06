"""
v1 / naive strategy: take every file referenced in the traceback, plus
their direct imports one level deep. Exposed behind a stable function
signature so a smarter (embedding or dependency-graph based) retriever
can be swapped in later without touching ai_service.py.
"""
import ast
from pathlib import Path


def get_relevant_files(project_path: Path, errors: list[dict]) -> list[Path]:
    seen: set[Path] = set()

    for error in errors:
        if not error.get("file_path"):
            continue
        f = Path(error["file_path"])
        if f.exists():
            seen.add(f)
            seen.update(_direct_imports(f, project_path))

    return list(seen)


def _direct_imports(file_path: Path, project_root: Path) -> list[Path]:
    try:
        tree = ast.parse(file_path.read_text())
    except (SyntaxError, OSError):
        return []

    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            candidate = project_root / (node.module.replace(".", "/") + ".py")
            if candidate.exists():
                found.append(candidate)
    return found
