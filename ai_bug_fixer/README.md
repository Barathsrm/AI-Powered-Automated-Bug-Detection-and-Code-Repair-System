# AI Bug Fixer

Uploads a Python project, runs it in an isolated Docker sandbox, and uses
an AI repair loop to detect and fix failing tests.

## Setup

    cd backend
    pip install -r requirements.txt
    docker build -f ../docker/python_runner.Dockerfile -t python_runner:latest .
    uvicorn main:app --reload

Start Redis and a Celery worker for the analysis/repair background jobs:

    docker run -p 6379:6379 redis:7-alpine
    celery -A services.execution_service.celery_app worker --loglevel=info

## Status

Scaffold stage. Core structure, auth, sandboxed execution, and the AI
repair loop are wired up; TODOs remain in tests/ and in ai_service.py's
prompt design.
