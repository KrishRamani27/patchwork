from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from backend.agents.state import FixerState
from backend.graph import app as graph_app

api = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

api.add_middleware(
    CORSMiddleware,
    allow_origins=["https://patchwork-hazel.vercel.app"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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