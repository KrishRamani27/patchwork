from langgraph.graph import StateGraph, END
from backend.agents.state import FixerState
from backend.agents.writer import writer
from backend.agents.runner import runner
from backend.agents.fixer import fixer

def router(state:FixerState) -> str:
    if state["result"]=="passed":
        return "done"
    elif state["attempts"]>=5:
        return "give_up"
    else:
        return "fix"


def give_up(state: FixerState) -> FixerState:
    state["result"] = f"FAILED after 5 attempts. Last error:\n{state['result']}"
    return state

#Added Graph with all the nodes initialized
graph=StateGraph(FixerState)
graph.add_node("writer",writer)
graph.add_node("runner",runner)
graph.add_node("fixer",fixer)
graph.add_node("give_up",give_up)

graph.set_entry_point("writer")


#Adding Edges
graph.add_edge("writer","runner")
graph.add_conditional_edges(
    "runner",
    router,
    {
        "done": END,
        "fix": "fixer",
        "give_up": "give_up"
    }
)

graph.add_edge("fixer", "runner")
graph.add_edge("give_up", END)

app = graph.compile()