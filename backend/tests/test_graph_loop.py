from agents.state import FixerState
from graph import app

initial_state: FixerState = {
    "task": "Write a function count_vowels(s) that counts vowels (a,e,i,o,u) in a string. The letter y counts as a vowel ONLY when it is not the first character of the string.",
    "tests": 'assert count_vowels("yellow") == 2\nassert count_vowels("sky") == 1\nassert count_vowels("aey") == 2\nassert count_vowels("apple") == 2',
    "code": "",
    "result": "",
    "attempts": 0
}

for step in app.stream(initial_state):
    node_name = list(step.keys())[0]
    print(f"--- ran node: {node_name} ---")

final_state = app.invoke(initial_state)
print("\n=== RESULT ===", final_state["result"])
print("=== ATTEMPTS ===", final_state["attempts"])