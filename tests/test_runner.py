from agents.state import FixerState
from agents.writer import writer
from agents.runner import runner

state: FixerState = {
    "task": "Write a function called reverse_string that takes a string and returns it reversed",
    "tests": 'assert reverse_string("hello") == "olleh"\nassert reverse_string("racecar") == "racecar"\nassert reverse_string("") == ""',
    "code": "",
    "result": "",
    "attempts": 0
}

state = writer(state)
print("GENERATED CODE:\n", state["code"])
state = runner(state)
print("\nRESULT:", state["result"])