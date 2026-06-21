import os
from dotenv import load_dotenv
from anthropic import Anthropic
from state import FixerState

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def writer(state: FixerState) -> FixerState:
    prompt = f""" Write Python code for this task:
    {state["task"]}
    Respond with ONLY the code, no other text.
    """
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1000,
        temperature=0.0,
        messages=[{"role": "user","content": prompt}]
    )
    state["code"] = response.content[0].text
    return state