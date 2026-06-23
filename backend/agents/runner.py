import subprocess
import tempfile
import os
from backend.agents.state import FixerState
from backend.agents.utils import strip_code

USE_DOCKER = os.getenv("USE_DOCKER", "false").lower() == "true"

def run_with_docker(temp_dir: str, temp_name: str):
    return subprocess.run(
        [
            "docker", "run", "--rm",
            "--network", "none",
            "-v", f"{temp_dir}:/sandbox",
            "patchwork-sandbox",
            "python", f"/sandbox/{temp_name}"
        ],
        capture_output=True,
        text=True,
        timeout=10
    )

def run_with_subprocess(temp_path: str):
    return subprocess.run(
        ["python", temp_path],
        capture_output=True,
        text=True,
        timeout=10
    )

def runner(state: FixerState) -> FixerState:
    code = strip_code(state["code"])
    full_script = code + "\n\n" + state["tests"]
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full_script)
        temp_path = f.name
        temp_dir = os.path.dirname(temp_path)
        temp_name = os.path.basename(temp_path)
    try:
        if USE_DOCKER:
            result = run_with_docker(temp_dir, temp_name)
        else:
            result = run_with_subprocess(temp_path)
        if result.returncode == 0:
            state["result"] = "passed"
        else:
            state["result"] = result.stderr
    except subprocess.TimeoutExpired:
        state["result"] = "timed out"
    finally:
        os.remove(temp_path)
    return state