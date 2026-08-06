from sqlmodel import Session

from models.analysis import Analysis, AnalysisStatus
from models.patch import Patch
from services.context_retriever import get_relevant_files
from services.ai_service import generate_patch
from services.validation_service import validate_patch
from utils.logger import get_logger

logger = get_logger(__name__)


def run_repair_loop(analysis: Analysis, project, errors: list[dict], session: Session) -> None:
    from pathlib import Path

    project_path = Path(project.storage_path)

    while analysis.attempt_count < analysis.max_attempts and analysis.tokens_used < analysis.token_budget:
        analysis.attempt_count += 1
        session.add(analysis)
        session.commit()

        error = errors[0]
        files = get_relevant_files(project_path, errors)
        file_contents = {str(f): f.read_text() for f in files}

        result = generate_patch(error, file_contents)
        analysis.tokens_used += result["tokens_used"]

        patch = Patch(
            analysis_id=analysis.id,
            attempt_number=analysis.attempt_count,
            file_path=error.get("file_path") or "unknown",
            diff=result["raw_response"],
            explanation=result["raw_response"],
        )
        session.add(patch)
        session.add(analysis)
        session.commit()
        session.refresh(patch)

        success, remaining_errors = validate_patch(patch, project_path)
        patch.validated = success
        session.add(patch)
        session.commit()

        if success:
            analysis.status = AnalysisStatus.success
            session.add(analysis)
            session.commit()
            return

        errors = remaining_errors or errors

    analysis.status = AnalysisStatus.failed
    session.add(analysis)
    session.commit()
    logger.info("Repair loop ended without success for analysis %s", analysis.id)
