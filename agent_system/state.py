"""Shared typed state for the LangGraph workflow."""
from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    # Conversation / trace
    messages: List[Dict[str, Any]]
    trace_log: List[Dict[str, Any]]

    # User spec
    spec: Dict[str, Any]

    # Design
    current_stackup: List[Dict[str, Any]]
    seed_index: int
    last_guardrail_ok: bool

    # Results
    electrical_results: Dict[str, Any]
    thermal_results: Dict[str, Any]

    # Pools
    solution_pool: List[Dict[str, Any]]

    # Control
    iteration_count: int
    status: str
    research_context: str

    # Output
    final_solutions: List[Dict[str, Any]]
    guardrail_notes: str