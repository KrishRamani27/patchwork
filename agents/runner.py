import subprocess
import tempfile
import os
from agents.state import FixerState
from agents.utils import strip_code

def runner(state: FixerState) -> FixerState:
    code = strip_code(state["code"])
    full_script=code+"\n\n"+state["tests"] #Combining the code and the tests into a single script
    #Creating a temporary file to run the script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full_script)
        temp_path=f.name
        temp_dir = os.path.dirname(temp_path)
        temp_name = os.path.basename(temp_path)

    try:
        #Running the script
        result = subprocess.run(
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
        #Checking if the script passed
        if result.returncode == 0:
            state["result"] = "passed"
        else:
            state["result"]= result.stderr
    except subprocess.TimeoutExpired:
        state["result"] = "timed out"
    finally:
        os.remove(temp_path)
    return state