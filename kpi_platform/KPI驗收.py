"""KPI 平台：各階段 KPI 驗收程式。"""

import sys

sys.path.insert(0, "/home/sam/代理人")
from kpi_platform.驗證 import 驗證阻抗, 驗證熱負載, 驗證串擾


def 驗收KPI1():
    """KPI-1：雲端 AI 計算平台 — 阻抗/疊構/損耗/視覺化。"""
    r1 = 驗證阻抗(12.0, 1.4, 8.0, 4.2, "NbTi", 0.01)
    r2 = 驗證熱負載(
        {"material": "NbTi", "width_mil": 12.0, "thickness_mil": 1.4},
        [
            {
                "stage_name": "MC",
                "temp_k": 0.01,
                "line_length_m": 0.1,
                "attenuation_db": 20,
            }
        ],
    )
    r3 = 驗證串擾({"freq_ghz": 6.0, "coupling_length_mm": 100, "spacing_um": 100})
    return {
        "kpi": "KPI-1",
        "阻抗": r1,
        "熱負載": r2,
        "串擾": r3,
        "pass": r1["pass"] and r2["pass"],
    }


def 驗收KPI3():
    """KPI-3：電性 SOP — S11/S21/串擾。"""
    r = 驗證串擾(
        {"freq_ghz": 6.0, "coupling_length_mm": 100, "spacing_um": 100},
        next_limit=-30.0,
        fext_limit=-20.0,
    )
    return {"kpi": "KPI-3", "串擾": r, "pass": r["pass"]}


def 驗收KPI4():
    """KPI-4：熱負載 SOP — 300K/150K/40K。"""
    stages = [
        {
            "stage_name": "300K",
            "temp_k": 300.0,
            "line_length_m": 0.5,
            "attenuation_db": 0,
        },
        {
            "stage_name": "150K",
            "temp_k": 150.0,
            "line_length_m": 0.3,
            "attenuation_db": 5,
        },
        {
            "stage_name": "40K",
            "temp_k": 40.0,
            "line_length_m": 0.2,
            "attenuation_db": 10,
        },
    ]
    r = 驗證熱負載(
        {"material": "NbTi", "width_mil": 12.0, "thickness_mil": 1.4},
        stages,
        budget_uw=100.0,
    )
    return {"kpi": "KPI-4", "熱負載": r, "pass": r["pass"]}


def 驗收全部():
    return [驗收KPI1(), 驗收KPI3(), 驗收KPI4()]
