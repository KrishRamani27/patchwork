import os
from state import FixerState
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
client=Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def fixer(state: FixerState) -> FixerState:
    prompt=f""" This python code failed. please fix it.
    TASK: {state["task"]}
    CODE: {state["code"]}
    ERROR: {state["result"]}
    Respond ONLY with corrected code, no explainations, no markdown."""

    response=client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0.3,
        messages=[{"role": "user", "content": prompt}]
    )

    state["code"]=response.content[0].text
    state["attempts"]+=1
    return state
