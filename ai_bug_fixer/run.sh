#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Build frontend
cd "$ROOT_DIR/frontend"
echo "Building frontend..."
npm run build

# Copy build into backend static folder
BACKEND_DIST="$ROOT_DIR/backend/frontend_dist"
rm -rf "$BACKEND_DIST"
mkdir -p "$BACKEND_DIST"
cp -r "$ROOT_DIR/frontend/dist/." "$BACKEND_DIST/"

echo "Starting backend on port 5173 (serving frontend)..."
cd "$ROOT_DIR/backend"

# Prefer virtualenv python if present
VENV_PY="$ROOT_DIR/backend/.venv/bin/python"
if [ -x "$VENV_PY" ]; then
	PYTHON="$VENV_PY"
else
	PYTHON="$(command -v python || command -v python3)"
fi

exec "$PYTHON" -m uvicorn main:app --host 0.0.0.0 --port 5173
