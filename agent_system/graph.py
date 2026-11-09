"""Build the LangGraph workflow with SQLite checkpointing."""

from langgraph.graph import StateGraph, START, END

try:
    import sqlite3
    from langgraph.checkpoint.sqlite import SqliteSaver

    _HAS_SQLITE = True
except Exception:
    _HAS_SQLITE = False
    from langgraph.checkpoint.memory import MemorySaver

from .state import AgentState
from .nodes import (
    researcher_node,
    init_design_node,
    physicist_node,
    guardrail_node,
    optimizer_node,
    solution_adder_node,
    reporter_node,
    should_continue,
)
from .config import CHECKPOINT_DB


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("researcher", researcher_node)
    g.add_node("init_design", init_design_node)
    g.add_node("physicist", physicist_node)
    g.add_node("guardrail", guardrail_node)
    g.add_node("solution_adder", solution_adder_node)
    g.add_node("optimizer", optimizer_node)
    g.add_node("reporter", reporter_node)

    g.add_edge(START, "researcher")
    g.add_edge("researcher", "init_design")
    g.add_edge("init_design", "physicist")
    g.add_edge("physicist", "guardrail")

    # conditional: approve -> add solution; reject -> optimizer; terminate if max iters
    def after_guardrail(state: AgentState) -> str:
        from .config import MAX_ITERATIONS

        if state.get("iteration_count", 0) >= MAX_ITERATIONS:
            return "report"
        return "add" if state.get("last_guardrail_ok") else "optimize"

    g.add_conditional_edges(
        "guardrail",
        after_guardrail,
        {"add": "solution_adder", "optimize": "optimizer", "report": "reporter"},
    )

    # after adding solution, check termination
    def after_add(state: AgentState) -> str:
        pool = state.get("solution_pool", [])
        it = state.get("iteration_count", 0)
        from .config import MAX_ITERATIONS, SOLUTION_POOL_TARGET

        if len(pool) >= SOLUTION_POOL_TARGET or it >= MAX_ITERATIONS:
            return "report"
        return "optimize"

    g.add_conditional_edges(
        "solution_adder", after_add, {"report": "reporter", "optimize": "optimizer"}
    )

    g.add_edge("optimizer", "physicist")

    g.add_edge("reporter", END)

    if _HAS_SQLITE:
        conn = sqlite3.connect(CHECKPOINT_DB, check_same_thread=False)
        checkpointer = SqliteSaver(conn)
    else:
        checkpointer = MemorySaver()
    return g.compile(checkpointer=checkpointer)


def run(spec: dict, thread_id: str = "default") -> dict:
    graph = build_graph()
    cfg = {"configurable": {"thread_id": thread_id}}
    init = {
        "spec": spec,
        "trace_log": [],
        "messages": [],
        "solution_pool": [],
        "iteration_count": 0,
        "seed_index": 0,
    }
    return graph.invoke(init, config=cfg)
