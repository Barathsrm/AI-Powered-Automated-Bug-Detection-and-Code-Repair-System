from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import upload_routes, analysis_routes, repair_routes, report_routes, auth_routes
from database.database import init_db
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="AI Bug Fixer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(upload_routes.router, prefix="/upload", tags=["upload"])
app.include_router(analysis_routes.router, prefix="/analysis", tags=["analysis"])
app.include_router(repair_routes.router, prefix="/repair", tags=["repair"])
app.include_router(report_routes.router, prefix="/report", tags=["report"])


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/health")
def health():
    return {"status": "ok"}


# Serve built frontend if available (single-port mode)
frontend_dist = os.path.join(os.path.dirname(__file__), "frontend_dist")
if os.path.isdir(frontend_dist):
    app.mount("/", StaticFiles(directory=frontend_dist, html=True), name="frontend")
