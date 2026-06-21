import subprocess
import tempfile
import os
from state import FixerState

def strip_code(code: str) -> str:
    code = code.strip()
    if code.startswith("```"):
        lines = code.split("\n")
        lines = lines[1:]
        if lines and lines[-1].strip().startswith("```"):
            lines =lines[:-1]
        code = "\n".join(lines)
    return code

def runner(state: FixerState) -> FixerState:
    code = strip_code(state["code"])
    full_script=code+"\n\n"+state["tests"] #Combining the code and the tests into a single script
    #Creating a temporary file to run the script
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(full_script)
        temp_path=f.name

    try:
        #Running the script
        result = subprocess.run(["python", temp_path], capture_output=True, text=True,timeout=10)
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