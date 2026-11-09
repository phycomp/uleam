"""材質數據庫：材料屬性與驗收標準。"""

MATERIALS = {
    "Cu": {
        "tc_k": None,
        "resistivity_nohm_m": 1.7e-8,
        "thermal_a": 0.1,
        "thermal_b": 1.0,
        "density_g_cm3": 8.96,
        "category": "conductor",
    },
    "NbTi": {
        "tc_k": 9.2,
        "resistivity_nohm_m": 0.0,
        "thermal_a": 0.0005,
        "thermal_b": 1.5,
        "density_g_cm3": 6.0,
        "category": "superconductor",
    },
    "Nb": {
        "tc_k": 9.2,
        "resistivity_nohm_m": 0.0,
        "thermal_a": 0.002,
        "thermal_b": 1.3,
        "density_g_cm3": 8.57,
        "category": "superconductor",
    },
    "Ag": {
        "tc_k": None,
        "resistivity_nohm_m": 1.6e-8,
        "thermal_a": 0.4,
        "thermal_b": 1.0,
        "density_g_cm3": 10.49,
        "category": "conductor",
    },
    "Al": {
        "tc_k": 1.2,
        "resistivity_nohm_m": 2.7e-8,
        "thermal_a": 0.01,
        "thermal_b": 1.2,
        "density_g_cm3": 2.70,
        "category": "superconductor",
    },
    "FR4": {
        "tc_k": None,
        "dk": 4.2,
        "df": 0.02,
        "density_g_cm3": 1.85,
        "category": "dielectric",
    },
    "Sapphire": {
        "tc_k": None,
        "dk": 9.4,
        "df": 0.0001,
        "density_g_cm3": 3.98,
        "category": "dielectric",
    },
    "Polyimide": {
        "tc_k": None,
        "dk": 3.2,
        "df": 0.008,
        "density_g_cm3": 1.42,
        "category": "dielectric",
    },
}


def 驗收材質(name, measured):
    """驗收材質：比對量測值與規格，回傳 pass/fail。"""
    spec = MATERIALS.get(name)
    if spec is None:
        return {"material": name, "pass": False, "reason": "未知材料"}
    results = {}
    all_pass = True
    for key, val in measured.items():
        if key in spec:
            # 簡單容差 ±10%
            if isinstance(spec[key], (int, float)) and spec[key] != 0:
                ok = abs(val - spec[key]) / abs(spec[key]) <= 0.10
            else:
                ok = val == spec[key]
            results[key] = {"spec": spec[key], "measured": val, "pass": ok}
            if not ok:
                all_pass = False
        else:
            results[key] = {"spec": None, "measured": val, "pass": None}
    return {"material": name, "pass": all_pass, "details": results}


def 列出材質(category=None):
    if category is None:
        return list(MATERIALS.keys())
    return [k for k, v in MATERIALS.items() if v.get("category") == category]
