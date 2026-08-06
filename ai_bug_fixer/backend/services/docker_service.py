"""
Runs untrusted, user-uploaded code inside a locked-down container.

Security constraints (do not relax these without a reason):
- network_mode="none": no outbound network access at all
- mem_limit / nano_cpus / pids_limit: resource caps against runaway or
  fork-bombing code
- read_only root filesystem, writable only via a size-capped tmpfs
- runs as a non-root uid, all Linux capabilities dropped
- hard wall-clock timeout enforced from the caller side, container is
  force-killed and removed in a finally block no matter what happens
"""
import docker
from docker.errors import ContainerError, APIError
from utils.logger import get_logger

logger = get_logger(__name__)
client = docker.from_env()

RUNNER_IMAGE = "python_runner:latest"
DEFAULT_TIMEOUT_SECONDS = 120


def run_in_sandbox(host_project_path: str, command: str, timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict:
    """
    Runs `command` against the project mounted from host_project_path.
    Returns {"exit_code": int, "logs": str, "timed_out": bool}.
    """
    container = None
    try:
        container = client.containers.run(
            image=RUNNER_IMAGE,
            command=command,
            volumes={host_project_path: {"bind": "/workspace", "mode": "rw"}},
            working_dir="/workspace",
            network_mode="none",
            mem_limit="512m",
            nano_cpus=1_000_000_000,  # 1 CPU
            pids_limit=100,
            read_only=True,
            tmpfs={"/tmp": "size=100m"},
            user="1000:1000",
            security_opt=["no-new-privileges"],
            cap_drop=["ALL"],
            detach=True,
        )
        try:
            result = container.wait(timeout=timeout)
            exit_code = result.get("StatusCode", 1)
            timed_out = False
        except Exception:
            container.kill()
            exit_code = 124
            timed_out = True

        logs = container.logs().decode("utf-8", errors="replace")
        return {"exit_code": exit_code, "logs": logs, "timed_out": timed_out}

    except (ContainerError, APIError) as e:
        logger.error("Docker execution failed: %s", e)
        return {"exit_code": 1, "logs": str(e), "timed_out": False}

    finally:
        if container is not None:
            try:
                container.remove(force=True)
            except Exception:
                pass


def build_runner_image(dockerfile_path: str = "docker/python_runner.Dockerfile") -> None:
    client.images.build(path=".", dockerfile=dockerfile_path, tag=RUNNER_IMAGE)
