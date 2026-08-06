"""
Long-running work (docker build, install, test, AI round trips) is handed
off to a Celery worker instead of blocking the request/response cycle -
this can take anywhere from seconds to several minutes.
"""
from celery import Celery
from sqlmodel import Session

from database.database import engine
from models.analysis import Analysis, AnalysisStatus
from models.project import Project

celery_app = Celery("ai_bug_fixer", broker="redis://localhost:6379/0", backend="redis://localhost:6379/0")


def queue_analysis(project_id: int, session: Session) -> Analysis:
    analysis = Analysis(project_id=project_id, status=AnalysisStatus.queued)
    session.add(analysis)
    session.commit()
    session.refresh(analysis)

    run_analysis_task.delay(analysis.id)
    return analysis


@celery_app.task
def run_analysis_task(analysis_id: int) -> None:
    from services.docker_service import run_in_sandbox
    from services.dependency_service import find_requirements_file, install_command_for
    from services.error_parser import parse_errors
    from services.patch_service import run_repair_loop

    with Session(engine) as session:
        analysis = session.get(Analysis, analysis_id)
        project = session.get(Project, analysis.project_id)

        analysis.status = AnalysisStatus.running
        session.add(analysis)
        session.commit()

        req_file = find_requirements_file(__import__("pathlib").Path(project.storage_path))
        run_in_sandbox(project.storage_path, install_command_for(req_file))

        test_result = run_in_sandbox(project.storage_path, "pytest --tb=short -q")
        errors = parse_errors(test_result["logs"])

        if not errors:
            analysis.status = AnalysisStatus.success
            session.add(analysis)
            session.commit()
            return

        analysis.status = AnalysisStatus.repairing
        session.add(analysis)
        session.commit()

        run_repair_loop(analysis, project, errors, session)
