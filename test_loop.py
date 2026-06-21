from state import FixerState
from runner import runner
from fixer import fixer

# Deliberately broken: doesn't handle n < 2, so is_prime(1) wrongly returns True
broken_code = """def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True"""

state: FixerState = {
    "task": "Write a function called is_prime(n) that returns True if n is prime, False otherwise. Numbers less than 2 are not prime.",
    "tests": 'assert is_prime(2) == True\nassert is_prime(7) == True\nassert is_prime(1) == False\nassert is_prime(0) == False\nassert is_prime(-5) == False',
    "code": broken_code,
    "result": "",
    "attempts": 0
}

# First run — guaranteed to fail
state = runner(state)
print("=== FIRST RUN (should fail) ===")
print(state["result"])

# Repair loop, up to 3 attempts
while state["result"] != "passed" and state["attempts"] < 3:
    print(f"\n=== FIXING (attempt {state['attempts'] + 1}) ===")
    state = fixer(state)
    print(state["code"])
    state = runner(state)
    print("\n=== RESULT ===")
    print(state["result"])

print(f"\n=== DONE after {state['attempts']} fix attempts: {state['result']} ===")