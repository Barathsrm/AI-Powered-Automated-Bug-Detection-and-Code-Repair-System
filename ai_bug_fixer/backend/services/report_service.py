from pathlib import Path
from sqlmodel import Session, select

from models.analysis import Analysis
from models.patch import Patch
from models.report import Report

REPORTS_DIR = Path(__file__).resolve().parent.parent / "generated_reports"


def generate_report(analysis_id: int, session: Session) -> Report:
    analysis = session.get(Analysis, analysis_id)
    patches = session.exec(select(Patch).where(Patch.analysis_id == analysis_id)).all()

    summary_lines = [
        f"Analysis #{analysis.id} - status: {analysis.status}",
        f"Attempts used: {analysis.attempt_count}/{analysis.max_attempts}",
        f"Tokens used: {analysis.tokens_used}/{analysis.token_budget}",
        "",
        "Patches:",
    ]
    for p in patches:
        summary_lines.append(f"  attempt {p.attempt_number} - {p.file_path} - validated={p.validated}")

    summary_text = "\n".join(summary_lines)

    REPORTS_DIR.mkdir(exist_ok=True)
    report_path = REPORTS_DIR / f"analysis_{analysis_id}.txt"
    report_path.write_text(summary_text)

    report = Report(analysis_id=analysis_id, file_path=str(report_path), summary=summary_text)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report
