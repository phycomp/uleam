"""LangGraph nodes. Each node logs a trace entry into state['trace_log']."""

import json
import time
from typing import Any, Dict

from .config import TARGET_ZO, MAX_ITERATIONS, SOLUTION_POOL_TARGET, MIN_THICKNESS_MIL
from .state import AgentState
from .tools import (
    calc_impedance_and_loss,
    calc_thermal_load,
    check_drc,
    check_guardrail,
    make_stackup,
    MATERIAL_MAP,
)


def _trace(
    state: AgentState, node: str, inp: Any, out: Any, decision: str = ""
) -> Dict:
    entry = {
        "node": node,
        "ts": time.time(),
        "input": inp,
        "output": out,
        "decision": decision,
    }
    log = list(state.get("trace_log", []))
    log.append(entry)
    return {"trace_log": log}


SEEDS = [
    ("Cu", 10.0, 20.0),  # room-temp copper
    ("NbTi", 6.0, 12.0),  # superconducting micro
    ("Nb", 4.0, 8.0),  # high-impedance Nb
]


def researcher_node(state: AgentState) -> Dict[str, Any]:
    spec = state.get("spec", {})
    try:
        from .llm import chat

        res = chat(
            "You are a microwave/quantum hardware researcher. Summarize material Dk, loss tangent, min thickness and symmetry concisely under 120 words.",
            f"Spec: {spec}",
        )
    except Exception as e:
        res = f"researcher error: {e}"
    out = {"research_context": res}
    out.update(_trace(state, "researcher", spec, res, "context gathered"))
    return out


def init_design_node(state: AgentState) -> Dict[str, Any]:
    spec = state.get("spec", {})
    # seed 0 initially
    mat, W, H = SEEDS[0]
    stackup = make_stackup(mat, W, H)
    out = {
        "current_stackup": stackup,
        "seed_index": 0,
        "iteration_count": 0,
        "solution_pool": [],
        "last_guardrail_ok": False,
    }
    out.update(_trace(state, "init_design", spec, stackup, "seed0"))
    return out


def physicist_node(state: AgentState) -> Dict[str, Any]:
    stackup = state["current_stackup"]
    # conductor layer
    cond = next((l for l in stackup if l.get("layer") == "conductor"), stackup[1])
    W = cond.get("width_mil", 10.0)
    H = stackup[0].get("thickness_mil", 20.0)
    mat = cond.get("material", "Cu")
    freq = state.get("spec", {}).get("freq", 8.0)
    elec = calc_impedance_and_loss(W, H, mat, freq)
    thermal = calc_thermal_load(stackup)
    out = {"electrical_results": elec, "thermal_results": thermal}
    out.update(
        _trace(
            state,
            "physicist",
            {"W": W, "H": H, "mat": mat},
            {"elec": elec, "thermal": thermal},
            "computed",
        )
    )
    return out


def guardrail_node(state: AgentState) -> Dict[str, Any]:
    elec = state["electrical_results"]
    thermal = state["thermal_results"]
    drc = check_drc(state["current_stackup"])
    gr = check_guardrail(elec, thermal, drc)
    ok = gr["ok"]
    review = "deterministic"
    notes = gr["notes"]
    out = {"last_guardrail_ok": ok, "guardrail_notes": notes}
    out.update(
        _trace(
            state,
            "guardrail",
            gr,
            {"ok": ok, "review": review},
            "APPROVE" if ok else "REJECT",
        )
    )
    return out


def _add_solution(state: AgentState) -> Dict[str, Any]:
    pool = list(state.get("solution_pool", []))
    pool.append(
        {
            "stackup": state["current_stackup"],
            "elec": state["electrical_results"],
            "thermal": state["thermal_results"],
            "iteration": state["iteration_count"],
        }
    )
    return {"solution_pool": pool}


def optimizer_node(state: AgentState) -> Dict[str, Any]:
    """Decide next stackup: if last ok -> next seed; else adjust current."""
    spec = state.get("spec", {})
    target = spec.get("target_zo", TARGET_ZO)
    last_ok = state.get("last_guardrail_ok", False)
    seed_idx = state.get("seed_index", 0)
    current = state["current_stackup"]
    cond = next((l for l in current if l.get("layer") == "conductor"), current[1])
    W = cond.get("width_mil", 10.0)
    H = current[0].get("thickness_mil", 20.0)
    mat = cond.get("material", "Cu")

    # Determine strategy deterministically (LLM not in control loop)
    elec = state["electrical_results"]
    thermal = state["thermal_results"]
    zo = elec.get("Zo", 50.0)
    thermal_ok = thermal.get("ok", True)

    if last_ok:
        if seed_idx + 1 < len(SEEDS):
            seed_idx += 1
            new_mat, new_W, new_H = SEEDS[seed_idx]
            action = "next_seed"
        else:
            # no more seeds: force termination
            new_mat, new_W, new_H = mat, W, H
            action = "done"
    else:
        # priority: if thermal fails, mutate material first
        if not thermal_ok and mat == "Cu":
            new_mat = "NbTi"
            new_W, new_H = W, H
            action = "mutate_material"
        elif not thermal_ok and mat == "NbTi":
            new_mat = "Nb"
            new_W, new_H = W, H
            action = "mutate_material"
        else:
            # geometry adjust: solve for H that yields target Zo (direct, deterministic)
            new_mat = mat
            Er = MATERIAL_MAP.get(mat, 3.38)
            T = 1.4
            try:
                import math

                target_ln = target * math.sqrt(Er + 1.41) / 87.0
                # solve for H given current W
                denom = 0.8 * W + T
                new_H = denom * math.exp(target_ln) / 5.98
                new_W = W
                # enforce min thickness: if H too small, fix H=min and solve for W
                if new_H < MIN_THICKNESS_MIL:
                    new_H = MIN_THICKNESS_MIL
                    # solve 5.98*H/(0.8*W+T) = exp(target_ln)
                    new_W = (5.98 * new_H / math.exp(target_ln) - T) / 0.8
            except Exception:
                new_H, new_W = H, W
            action = "adjust_geo"

    new_W = max(2.0, min(30.0, new_W))
    new_H = max(MIN_THICKNESS_MIL, min(50.0, new_H))

    stackup = make_stackup(new_mat, new_W, new_H)
    if action == "done":
        iter_count = 999
    else:
        iter_count = state.get("iteration_count", 0) + 1
    out = {
        "current_stackup": stackup,
        "seed_index": seed_idx,
        "iteration_count": iter_count,
    }
    out.update(
        _trace(
            state,
            "optimizer",
            {"last_ok": last_ok, "zo": zo},
            {
                "action": action,
                "mat": new_mat,
                "W": new_W,
                "H": new_H,
                "seed_idx": seed_idx,
            },
            action,
        )
    )
    return out


def solution_adder_node(state: AgentState) -> Dict[str, Any]:
    out = _add_solution(state)
    out.update(
        _trace(
            state,
            "solution_adder",
            state["electrical_results"],
            {"pool_size": len(out["solution_pool"])},
            "added",
        )
    )
    return out


def reporter_node(state: AgentState) -> Dict[str, Any]:
    pool = state.get("solution_pool", [])
    try:
        from .llm import chat

        report = chat(
            "You are a technical writer. Produce 3 solution variants (electrical-optimal, thermal-optimal, process-balanced) with material/W/H/Zo/thermal and one-line rationale. Under 200 words.",
            f"Solution pool: {pool}",
        )
    except Exception as e:
        report = f"reporter error: {e}"
    out = {
        "final_solutions": pool,
        "status": "done",
        "messages": [{"role": "assistant", "content": report}],
    }
    out.update(_trace(state, "reporter", {"pool_size": len(pool)}, report, "final"))
    return out


def should_continue(state: AgentState) -> str:
    pool = state.get("solution_pool", [])
    it = state.get("iteration_count", 0)
    if len(pool) >= SOLUTION_POOL_TARGET or it >= MAX_ITERATIONS:
        return "report"
    return "loop"


__all__ = ["researcher_node", "init_design_node", "physicist_node", "guardrail_node",
           "optimizer_node", "solution_adder_node", "reporter_node", "should_continue"]
