"""代理主程式：純 Python 狀態機（移除 langgraph 依賴）。

保留原 LangGraph 工作流的節點與決策邏輯：
Init -> ElecCalc -> ThermalCalc -> Review (loop) -> Generator -> END
"""
from copy import deepcopy

from 全域狀態 import AgentState
from 計算 import calculate_quantum_impedance, calculate_coupled_thermal_load


def init_design_node(state: AgentState) -> AgentState:
    # 節點 1：初始化設計（硬規則：必須對稱）
    s = deepcopy(state)
    if "current_stackup" not in s or not s.get("current_stackup"):
        s["current_stackup"] = [
            {"layer_id": 1, "name": "Top_Trace", "material": "Cu", "thickness_mil": 1.4, "width_mil": 5.0, "spacing_mil": 6.0},
            {"layer_id": 2, "name": "Dielectric", "material": "FR4", "thickness_mil": 4.0, "width_mil": 0.0, "spacing_mil": 0.0},
        ]
    s["iteration_count"] = 0
    s.setdefault("solution_pool", [])
    s.setdefault("target_zo", 50.0)
    s.setdefault("frequency_ghz", 6.0)
    s.setdefault("temperature_profile", [])
    return s


def electrical_calc_node(state: AgentState) -> AgentState:
    # 節點 2：電性模擬
    s = deepcopy(state)
    stackup = s["current_stackup"]
    trace = stackup[0] if isinstance(stackup, list) else stackup
    h = stackup[1]["thickness_mil"] if isinstance(stackup, list) and len(stackup) > 1 else 4.0
    res = calculate_quantum_impedance(
        width_mil=trace["width_mil"],
        thickness_mil=trace["thickness_mil"],
        h_mil=h,
        er=4.2,
        material=trace["material"],
        temp=0.01,
    )
    s["electrical_results"] = res
    return s


def thermal_calc_node(state: AgentState) -> AgentState:
    # 節點 3：熱負載耦合模擬
    s = deepcopy(state)
    stackup = s["current_stackup"]
    trace = stackup[0] if isinstance(stackup, list) else stackup
    stages = s.get("temperature_profile") or [
        {"stage_name": "300K", "temp_k": 300.0, "line_length_m": 0.1, "attenuation_db": 0.0},
        {"stage_name": "4K", "temp_k": 4.0, "line_length_m": 0.05, "attenuation_db": 0.0},
        {"stage_name": "MC_10mK", "temp_k": 0.01, "line_length_m": 0.02, "attenuation_db": 0.0},
    ]
    res = calculate_coupled_thermal_load(trace, stages)
    s["thermal_results"] = res
    return s


def quantum_coherence_review_node(state: AgentState) -> AgentState:
    # 節點 4：評審與優化決策
    s = deepcopy(state)
    zo = s["electrical_results"]["zo"]
    total_heat = s["thermal_results"]["total_load_w"]
    iter_idx = s["iteration_count"]

    is_zo_ok = 49.0 <= zo <= 51.0
    is_thermal_ok = total_heat < 10e-6

    if is_zo_ok and is_thermal_ok:
        s["solution_pool"].append({
            "stackup": deepcopy(s["current_stackup"]),
            "elec": s["electrical_results"],
            "thermal": s["thermal_results"],
        })

    if len(s["solution_pool"]) >= 3 or iter_idx >= 10:
        s["iteration_count"] = iter_idx + 1
        return s

    # 優化路徑決策
    next_stackup = deepcopy(s["current_stackup"])
    if not is_thermal_ok and is_zo_ok:
        trace = next_stackup[0] if isinstance(next_stackup, list) else next_stackup
        if trace["material"] == "Cu":
            trace["material"] = "NbTi"
        else:
            trace["width_mil"] -= 0.5
            if isinstance(next_stackup, list) and len(next_stackup) > 1:
                next_stackup[1]["thickness_mil"] -= 0.3

    s["current_stackup"] = next_stackup
    s["iteration_count"] = iter_idx + 1
    return s


def should_continue(state: AgentState) -> str:
    if len(state["solution_pool"]) >= 3 or state["iteration_count"] >= 10:
        return "generate_final"
    return "loop_optimize"


def solution_generator_node(state: AgentState) -> AgentState:
    # 節點 5：方案生成器
    s = deepcopy(state)
    pool = s.get("solution_pool", [])
    # 簡化：取前 3 套
    s["final_solutions"] = pool[:3]
    return s


def run_workflow(initial_state: AgentState, max_iter: int = 10) -> AgentState:
    state = init_design_node(initial_state)
    while True:
        state = electrical_calc_node(state)
        state = thermal_calc_node(state)
        state = quantum_coherence_review_node(state)
        decision = should_continue(state)
        if decision == "generate_final" or state["iteration_count"] >= max_iter:
            break
    state = solution_generator_node(state)
    return state


# 相容舊介面：提供 app 物件（可呼叫）
class _App:
    def invoke(self, initial_state, config=None):
        return run_workflow(initial_state)

    def compile(self):
        return self


app = _App()


if __name__ == "__main__":
    from 全域狀態 import AgentState
    demo_state = {
        "target_zo": 50.0,
        "frequency_ghz": 6.0,
        "temperature_profile": [],
        "current_stackup": [],
        "is_symmetric": True,
        "electrical_results": {},
        "thermal_results": {},
        "coherence_score": 0.0,
        "iteration_count": 0,
        "solution_pool": [],
    }
    result = run_workflow(demo_state)
    print("iterations:", result["iteration_count"])
    print("solutions:", len(result.get("solution_pool", [])))
    print("final:", result.get("final_solutions"))
