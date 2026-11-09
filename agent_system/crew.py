"""CrewAI role definitions (hybrid: used inside LangGraph nodes)."""
from crewai import Agent, LLM

from .config import OLLAMA_BASE_URL, OLLAMA_MODEL, TEMPERATURE


def make_llm():
    return LLM(model=f"ollama/{OLLAMA_MODEL}", base_url=OLLAMA_BASE_URL,
               temperature=TEMPERATURE)


def researcher_agent() -> Agent:
    return Agent(
        role="Researcher",
        goal="Gather material properties, process constraints and best practices for quantum transmission lines.",
        backstory="You are a microwave/quantum hardware researcher. You summarize material Dk, loss tangent, and DRC rules concisely.",
        llm=make_llm(), verbose=False, allow_delegation=False,
    )


def optimizer_agent() -> Agent:
    return Agent(
        role="Optimizer",
        goal="Propose and refine stackup (material + geometry) to meet Zo target and thermal budget.",
        backstory="You are a senior RF/quantum layout engineer. Priority: material mutation before geometry tweak. Never compute physics; delegate math to tools.",
        llm=make_llm(), verbose=False, allow_delegation=False,
    )


def guardrail_agent() -> Agent:
    return Agent(
        role="Guardrail Reviewer",
        goal="Review designs against Zo tolerance, DRC min thickness, and symmetry. Reject non-compliant designs with reasons.",
        backstory="You are a strict DRC reviewer. You only approve designs that satisfy all hard constraints.",
        llm=make_llm(), verbose=False, allow_delegation=False,
    )


def reporter_agent() -> Agent:
    return Agent(
        role="Reporter",
        goal="Produce three solution variants (electrical-optimal, thermal-optimal, process-balanced) with clear rationale.",
        backstory="You are a technical writer producing concise engineering reports.",
        llm=make_llm(), verbose=False, allow_delegation=False,
    )