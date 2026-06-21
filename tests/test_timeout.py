from state import FixerState
from runner import runner


state: FixerState = {
    "task": "infinite loop test",
    "tests": "",
    "code": "while True:\n    pass",
    "result": "",
    "attempts": 0
}

state = runner(state)
print("RESULT:", state["result"])