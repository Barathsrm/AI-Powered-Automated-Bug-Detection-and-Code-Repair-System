FROM python:3.12-slim

RUN useradd -m -u 1000 runner
WORKDIR /workspace

RUN pip install --no-cache-dir pytest

USER runner

# No CMD/ENTRYPOINT: docker_service.py supplies the command per run
# (install deps, then pytest), so the image stays generic.
