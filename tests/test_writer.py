from state import FixerState
from writer import writer

state: FixerState = {
    "task": "Write a function that reverses a string",
    "tests": "",
    "code": "",
    "result": "",
    "attempts": 0
}

result = writer(state)
print(result["code"])