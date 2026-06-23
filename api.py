from fastapi import FastAPI
from pydantic import BaseModel
from agents.state import FixerState
from graph import app as graph_app

api = FastAPI()

class SolveRequest(BaseModel):
    task: str
    tests: str

@api.post("/solve")
def solve(request: SolveRequest):
    initial_state: FixerState = {
        "task": request.task,
        "tests": request.tests,
        "code": "",
        "result": "",
        "attempts": 0
    }
    final_state = graph_app.invoke(initial_state)
    return {
        "code": final_state["code"],
        "result": final_state["result"],
        "attempts": final_state["attempts"]
    }