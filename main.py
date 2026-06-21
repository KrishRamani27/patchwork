from agents.state import FixerState
from graph import app
initial_state: FixerState = {
    "task": "Write a function called is_prime(n) that returns True if n is prime, False otherwise. Numbers less than 2 are not prime.",
    "tests": 'assert is_prime(2) == True\nassert is_prime(7) == True\nassert is_prime(1) == False\nassert is_prime(0) == False\nassert is_prime(-5) == False\nassert is_prime(13) == True',
    "code": "",
    "result": "",
    "attempts": 0
}

final_state = app.invoke(initial_state)

print("=== FINAL CODE ===")
print(final_state["code"])
print("\n=== FINAL RESULT ===")
print(final_state["result"])
print("\n=== ATTEMPTS ===")
print(final_state["attempts"])