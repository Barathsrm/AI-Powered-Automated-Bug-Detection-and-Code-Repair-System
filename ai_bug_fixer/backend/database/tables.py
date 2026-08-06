# Re-export all SQLModel table classes here so init_db() sees them
# when SQLModel.metadata.create_all() runs.
from models.user import User
from models.project import Project
from models.analysis import Analysis
from models.error import ErrorRecord
from models.patch import Patch
from models.report import Report

__all__ = ["User", "Project", "Analysis", "ErrorRecord", "Patch", "Report"]
