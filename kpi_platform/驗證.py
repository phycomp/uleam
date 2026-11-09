"""KPI 平台：驗證程式 + 測試數據。"""

import sys

sys.path.insert(0, "/home/sam/代理人")
from 計算 import calculate_quantum_impedance, calculate_coupled_thermal_load
from 串擾計算 import evaluate_crosstalk


def 驗證阻抗(width_mil, thickness_mil, h_mil, er, material, temp, target=50.0, tol=1.0):
    r = calculate_quantum_impedance(width_mil, thickness_mil, h_mil, er, material, temp)
    ok = abs(r["zo"] - target) <= tol
    return {"zo": r["zo"], "target": target, "tol": tol, "pass": ok, "detail": r}


def 驗證熱負載(stackup, stages, budget_uw=10.0):
    r = calculate_coupled_thermal_load(stackup, stages)
    heat_uw = r["total_load_w"] * 1e6
    ok = heat_uw <= budget_uw
    return {
        "heat_uw": round(heat_uw, 4),
        "budget_uw": budget_uw,
        "pass": ok,
        "detail": r,
    }


def 驗證串擾(spec, next_limit=-40.0, fext_limit=-30.0):
    r = evaluate_crosstalk(spec)
    ok = r["next_db"] <= next_limit and r["fext_db"] <= fext_limit
    return {
        "next_db": r["next_db"],
        "fext_db": r["fext_db"],
        "next_limit": next_limit,
        "fext_limit": fext_limit,
        "pass": ok,
    }


def 產生測試數據():
    """產生一組測試數據。"""
    return {
        "impedance": 驗證阻抗(12.0, 1.4, 8.0, 4.2, "NbTi", 0.01),
        "thermal": 驗證熱負載(
            {"material": "NbTi", "width_mil": 12.0, "thickness_mil": 1.4},
            [
                {
                    "stage_name": "MC",
                    "temp_k": 0.01,
                    "line_length_m": 0.1,
                    "attenuation_db": 20,
                }
            ],
        ),
        "crosstalk": 驗證串擾(
            {"freq_ghz": 6.0, "coupling_length_mm": 100, "spacing_um": 100}
        ),
    }
